from fastapi import APIRouter, Query, Depends, HTTPException, status
from config.db_config import get_db
from crud.favorite import is_new_favorite, add_favorite, delete_favorite, get_favorite, clear_favorite
from schemas.favorite import FavoriteCheckResponse, Favorite_userid, FavoriteResponse, FavoriteAddResponse
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

#添加收藏
@router.post("/add")
async def add_news_favorite(
        news_id: Favorite_userid,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
):
    favorite = await add_favorite(db=db, user_id=user.id, news_id=news_id.news_id)
    data = FavoriteAddResponse.model_validate(favorite)
    return success_response(message="success", data=data)

#取消收藏
@router.delete("/remove")
async def remove_news_favorite(
        news_id: int = Query(...,alias= "newsId"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
):
    result = await delete_favorite(db=db, news_id= news_id, user_id=user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录找不到")
    return success_response(message="success")

#获取收藏列表
@router.get("/list")
async def get_list_favorite(
        page: int = Query(default=1, ge= 1),
        page_size: int = Query(default=10, ge= 1, le=100, alias="pageSize"),
        db: AsyncSession = Depends(get_db),
        data: User = Depends(get_current_user),
):
    #调用方法
    rows, total = await get_favorite(db=db, user_id=data.id, page=page, page_size=page_size)
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id,
    }for news, favorite_time, favorite_id in rows]
    hasmore = total > page * page_size
    data = FavoriteResponse(list= favorite_list, total= total, hasMore= hasmore)
    return success_response(message="收藏列表获取成功", data=data)

#清空收藏列表
@router.delete("/clear")
async def clear_favorite_list(
        db: AsyncSession = Depends(get_db),
        data: User = Depends(get_current_user),
):
    rowcount = await clear_favorite(db=db, user_id=data.id)
    return success_response(message=f"收藏列表清空{rowcount}条数据")