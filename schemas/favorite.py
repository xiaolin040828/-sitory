from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

#添加请求题类型
class Favorite_userid(BaseModel):
    news_id: int = Field(..., alias="newsId")


class FavoriteNewsResponse(NewsItemBase):
    favorite_id: int = Field(..., alias="favoriteId")
    favorite_time: datetime = Field(..., alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class FavoriteAddResponse(BaseModel):
    id: int
    news_id: int = Field(alias="newsId")
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


#定义收藏类表响应的模型类
class FavoriteResponse(BaseModel):
    list: list[FavoriteNewsResponse]
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name= True,
        from_attributes= True,
    )
