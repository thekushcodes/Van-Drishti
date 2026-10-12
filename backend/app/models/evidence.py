from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)

    detection_id: Mapped[int | None] = mapped_column(
        ForeignKey("detections.id"),
        nullable=True,
        index=True,
    )

    evidence_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    kind: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    uri: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )