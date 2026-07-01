from fastapi import APIRouter, Query, Depends
from config.db_config import get_db
from utils.auth import get_current_user
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

@router.get("/check")
async def check_favorite(
        mews_id: int = Query(..., alias="newsId",description="新闻ID"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return success_response(message= "查询成功")