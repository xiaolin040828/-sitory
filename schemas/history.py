from pydantic import BaseModel, Field


class History_newsid(BaseModel):
    news_id: int = Field(..., alias="newsId")

from pydantic import ConfigDict
from datetime import datetime


class HistoryAddResponse(BaseModel):
    id: int
    news_id: int = Field(alias="newsId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
