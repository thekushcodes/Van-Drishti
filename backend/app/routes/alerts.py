from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"],
)


@router.get("")
def get_alerts(
    run_id: int,
    db: Session = Depends(get_db),
):
    alerts = (
        db.query(Alert)
        .filter(Alert.analysis_run_id == run_id)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return [
        {
            "alert_id": alert.alert_id,
            "analysis_run_id": alert.analysis_run_id,
            "severity": alert.severity,
            "message": alert.message,
            "created_at": alert.created_at.isoformat(),
        }
        for alert in alerts
    ]