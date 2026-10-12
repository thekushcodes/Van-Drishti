from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.intelligence_run import IntelligenceRun


router = APIRouter(
    prefix="/api/v1/reviews",
    tags=["Reviews"],
)


@router.get("")
def get_review_items(
    run_id: int,
    status: str = "open",
    db: Session = Depends(get_db),
):
    intelligence_run = (
        db.query(IntelligenceRun)
        .filter(IntelligenceRun.analysis_run_id == run_id)
        .order_by(IntelligenceRun.id.desc())
        .first()
    )

    if intelligence_run is None:
        raise HTTPException(
            status_code=404,
            detail="No intelligence run found for this analysis run",
        )

    response = requests.get(
        f"{settings.m4_url}/api/v1/intelligence/review-items",
        params={
            "status": status,
            "run_id": intelligence_run.m4_run_id,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()

from pydantic import BaseModel, Field


class ResolveReviewRequest(BaseModel):
    resolution_note: str = Field(min_length=1)


@router.post("/{review_id}/resolve")
def resolve_review_item(
    review_id: str,
    resolution: ResolveReviewRequest,
):
    try:
        response = requests.post(
            f"{settings.m4_url}/api/v1/intelligence/review-items/{review_id}/resolve",
            json=resolution.model_dump(),
            timeout=30,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to M4: {exc}",
        ) from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()
