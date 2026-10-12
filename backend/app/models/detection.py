from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_run_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_runs.id"),
        nullable=False,
        index=True,
    )

    event_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    species: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    detection_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    frame_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    x1: Mapped[float | None] = mapped_column(Float)
    y1: Mapped[float | None] = mapped_column(Float)
    x2: Mapped[float | None] = mapped_column(Float)
    y2: Mapped[float | None] = mapped_column(Float)