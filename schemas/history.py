from pydantic import BaseModel, Field


class History_newsid(BaseModel):
    news_id: int = Field(..., alias="newsId")