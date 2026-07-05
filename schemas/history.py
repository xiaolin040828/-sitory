from typing import List

from pydantic import BaseModel, Field
from schemas.base import NewsItemBase

class History_newsid(BaseModel):
    news_id: int = Field(..., alias="newsId")

from pydantic import ConfigDict
from datetime import datetime


class HistoryAddResponse(BaseModel):
    id: int
    news_id: int = Field(alias="newsId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)



class HistoryNewsResponse(NewsItemBase):
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryListResponse(BaseModel):
    list: List[HistoryNewsResponse]
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

