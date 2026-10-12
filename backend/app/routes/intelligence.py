from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.intelligence_run import IntelligenceRun


router = APIRouter(
    prefix="/api/v1/analysis-runs",
    tags=["Intelligence"],
)


@router.get("/{run_id}/intelligence")
def get_intelligence_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    intelligence_run = (
        db.query(IntelligenceRun)
        .filter(
            IntelligenceRun.analysis_run_id == run_id
        )
        .order_by(IntelligenceRun.id.desc())
        .first()
    )

    if intelligence_run is None:
        raise HTTPException(
            status_code=404,
            detail="Intelligence result not found",
        )

    return {
        "id": intelligence_run.id,
        "analysis_run_id": intelligence_run.analysis_run_id,
        "m4_run_id": intelligence_run.m4_run_id,
        "status": intelligence_run.status,
        "report_title": intelligence_run.report_title,
        "report_narrative": intelligence_run.report_narrative,
        "created_at": intelligence_run.created_at,
    }