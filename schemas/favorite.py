from pydantic import BaseModel, Field


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

#添加请求题类型
class Favorite_userid(BaseModel):
    user_id: int = Field(..., alias="userId")