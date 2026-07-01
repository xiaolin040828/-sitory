from fastapi import APIRouter, Query, Depends, HTTPException, status
from config.db_config import get_db
from crud.favorite import is_new_favorite
from schemas.favorite import FavoriteCheckResponse
from utils.auth import get_current_user
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId",description="新闻ID"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    bool = await is_new_favorite(user_id= user.id, news_id=news_id, db=db)
    if not bool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户没有收藏")

    return success_response(message= "查询成功", data=FavoriteCheckResponse(isFavorite=bool))