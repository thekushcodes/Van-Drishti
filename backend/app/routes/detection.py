from app.services.m4_payload import build_m4_payload

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.yolo_detector import YOLODetector
from app.models.analysis_run import AnalysisRun

from datetime import datetime, timezone

from app.services.m4_client import M4Client

from app.models.intelligence_run import IntelligenceRun


router = APIRouter(
    prefix="/api/v1/analysis-runs",
    tags=["Detection"],
)


@router.post("/{run_id}/process")

@router.post("/{run_id}/process")
def process_analysis_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis run not found",
        )

    if analysis_run.source_type != "video":
        raise HTTPException(
            status_code=400,
            detail="Only video analysis is supported currently",
        )

    if not analysis_run.source_name:
        raise HTTPException(
            status_code=400,
            detail="Analysis run has no source video",
        )

    detector = YOLODetector()

    output_path = detector.process_video(
        video_path=analysis_run.source_name,
        analysis_run_id=analysis_run.id,
        db=db,
    )

    analysis_run.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(analysis_run)

    payload = build_m4_payload(
        db=db,
        analysis_run=analysis_run,
    )

    client = M4Client()

    try:
        intelligence_result = client.create_intelligence_run(payload)
        report = intelligence_result.get("report", {})

        intelligence_run = IntelligenceRun(
            analysis_run_id=analysis_run.id,
            m4_run_id=intelligence_result["run_id"],
            status=intelligence_result["status"],
            report_title=report.get("title"),
            report_narrative=report.get("narrative"),
            created_at=datetime.now(timezone.utc),
        )

        db.add(intelligence_run)
        db.commit()
        db.refresh(intelligence_run)

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail=f"M4 request failed: {exc}",
        ) from exc

    return {
        "status": "completed",
        "analysis_run_id": analysis_run.id,
        "source_name": analysis_run.source_name,
        "output_video": output_path,
        "intelligence": intelligence_result,
    }

@router.get("/{run_id}/m4-payload")
def preview_m4_payload(
    run_id: int,
    db: Session = Depends(get_db),
):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis run not found",
        )

    return build_m4_payload(
        db=db,
        analysis_run=analysis_run,
    )
@router.post("/{run_id}/intelligence")
def create_intelligence_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis run not found",
        )

    payload = build_m4_payload(
        db=db,
        analysis_run=analysis_run,
    )

    client = M4Client()

    try:
        result = client.create_intelligence_run(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"M4 request failed: {exc}",
        )

    report = result.get("report", {})

    intelligence_run = IntelligenceRun(
        analysis_run_id=analysis_run.id,
        m4_run_id=result["run_id"],
        status=result["status"],
        report_title=report.get("title"),
        report_narrative=report.get("narrative"),
        created_at=datetime.now(timezone.utc),
    )

    db.add(intelligence_run)
    db.commit()
    db.refresh(intelligence_run)

    return result

@router.post("/{run_id}/analyze")
def analyze_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis run not found",
        )

    if analysis_run.source_type != "video":
        raise HTTPException(
            status_code=400,
            detail="Only video analysis is supported currently",
        )

    if not analysis_run.source_name:
        raise HTTPException(
            status_code=400,
            detail="Analysis run has no source video",
        )

    detector = YOLODetector()

    output_path = detector.process_video(
        video_path=analysis_run.source_name,
        analysis_run_id=analysis_run.id,
        db=db,
    )

    analysis_run.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(analysis_run)

    payload = build_m4_payload(
        db=db,
        analysis_run=analysis_run,
    )

    client = M4Client()

    try:
        intelligence_result = client.create_intelligence_run(
            payload
        )
        report = intelligence_result.get("report", {})

        intelligence_run = IntelligenceRun(
            analysis_run_id=analysis_run.id,
            m4_run_id=intelligence_result["run_id"],
            status=intelligence_result["status"],
            report_title=report.get("title"),
            report_narrative=report.get("narrative"),
            created_at=datetime.now(timezone.utc),
        )

        db.add(intelligence_run)
        db.commit()
        db.refresh(intelligence_run)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"M4 request failed: {exc}",
        )

    return {
        "status": "completed",
        "analysis_run_id": analysis_run.id,
        "output_video": output_path,
        "intelligence": intelligence_result,
    }