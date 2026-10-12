from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalysisRunCreate(BaseModel):
    camera_id: int | None = None
    source_type: str
    source_name: str | None = None
    started_at: datetime
    ended_at: datetime | None = None


class AnalysisRunResponse(BaseModel):
    id: int
    camera_id: int | None
    source_type: str
    source_name: str | None
    started_at: datetime
    ended_at: datetime | None

    model_config = ConfigDict(from_attributes=True)