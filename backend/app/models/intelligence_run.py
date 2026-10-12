from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IntelligenceRun(Base):
    __tablename__ = "intelligence_runs"

    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_run_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_runs.id"),
        nullable=False,
        index=True,
    )

    m4_run_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    report_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    report_narrative: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )