from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_run_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_runs.id"),
        nullable=False,
        index=True,
    )

    alert_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )