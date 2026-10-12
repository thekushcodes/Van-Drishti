from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.detection import Detection
from collections import Counter


router = APIRouter(
    prefix="/api/v1/analysis-runs",
    tags=["Detections"],
)

@router.get("/{run_id}/detections/summary")
def get_detection_summary(
    run_id: int,
    db: Session = Depends(get_db),
):
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

    return {
        "analysis_run_id": run_id,
        "total_detections": len(detections),
        "species_counts": dict(species_counts),
        "average_confidence": average_confidence,
    }

@router.get("/{run_id}/detections")
def get_detections(
    run_id: int,
    db: Session = Depends(get_db),
):
    detections = db.scalars(
        select(Detection)
        .where(Detection.analysis_run_id == run_id)
        .order_by(Detection.frame_number)
    ).all()

    return [
        {
            "event_id": detection.event_id,
            "timestamp": detection.timestamp,
            "species": detection.species,
            "confidence": detection.detection_confidence,
            "frame_number": detection.frame_number,
            "bounding_box": {
                "x1": detection.x1,
                "y1": detection.y1,
                "x2": detection.x2,
                "y2": detection.y2,
            },
        }
        for detection in detections
    ]