from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from pathlib import Path
import shutil
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.analysis_run import AnalysisRun

from sqlalchemy import select

from app.models.detection import Detection
from app.models.intelligence_run import IntelligenceRun
from collections import Counter


from app.database import get_db
from app.models.analysis_run import AnalysisRun
from app.schemas.analysis_run import (
    AnalysisRunCreate,
    AnalysisRunResponse,
)

router = APIRouter(
    prefix="/api/v1/analysis-runs",
    tags=["Analysis Runs"],
)


@router.post(
    "",
    response_model=AnalysisRunResponse,
    status_code=201,
)
def create_analysis_run(
    data: AnalysisRunCreate,
    db: Session = Depends(get_db),
):
    analysis_run = AnalysisRun(
        camera_id=data.camera_id,
        source_type=data.source_type,
        source_name=data.source_name,
        started_at=data.started_at,
        ended_at=data.ended_at,
    )

    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    return analysis_run
@router.post("/upload", status_code=201)
def upload_video(
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    video_path = upload_dir / video.filename

    with video_path.open("wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    analysis_run = AnalysisRun(
        source_type="video",
        source_name=str(video_path),
        started_at=datetime.now(timezone.utc),
    )

    db.add(analysis_run)
    db.commit()
    db.refresh(analysis_run)

    return {
        "analysis_run_id": analysis_run.id,
        "source_name": str(video_path),
        "status": "uploaded",
    }
@router.get("/{run_id}/result")
def get_analysis_result(
    run_id: int,
    db: Session = Depends(get_db),
):
    analysis_run = db.get(AnalysisRun, run_id)

    if analysis_run is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis run not found",
        )

    detections = db.scalars(
        select(Detection)
        .where(Detection.analysis_run_id == run_id)
    ).all()

    species_counts = Counter(
        detection.species
        for detection in detections
    )

    average_confidence = (
        sum(d.detection_confidence for d in detections)
        / len(detections)
        if detections
        else 0
    )

    intelligence_run = (
        db.query(IntelligenceRun)
        .filter(
            IntelligenceRun.analysis_run_id == run_id
        )
        .order_by(IntelligenceRun.id.desc())
        .first()
    )

    output_video = None

    if analysis_run.source_name:
        video_name = Path(analysis_run.source_name).stem
        output_video = f"/outputs/{video_name}_detected.mp4"

    return {
        "analysis_run_id": run_id,
        "status": "completed" if analysis_run.ended_at else "processing",
        "source_name": analysis_run.source_name,
        "output_video": output_video,
        "detections": {
            "total": len(detections),
            "species_counts": dict(species_counts),
            "average_confidence": average_confidence,
        },
        "intelligence": (
            {
                "m4_run_id": intelligence_run.m4_run_id,
                "status": intelligence_run.status,
                "title": intelligence_run.report_title,
                "narrative": intelligence_run.report_narrative,
            }
            if intelligence_run
            else None
        ),
    }