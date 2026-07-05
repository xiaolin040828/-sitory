from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from config.db_config import get_db
from schemas.history import History_newsid, HistoryAddResponse, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud.history import add_history, get_history
router = APIRouter(prefix="/api/history", tags=["history"])

#添加历史记录
@router.post("/add")
async def post_add_history(
        news_id : History_newsid,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    data = await add_history(db=db, user_id=user.id, news_id=news_id.news_id)
    result = HistoryAddResponse.model_validate(data)
    return success_response(message="添加成功", data=result)


#获取浏览历史列表
@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, le=100, alias='pageSize'),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    history, total = await get_history(page=page, page_size=page_size, user_id=user.id, db=db)
    hasmore = total > page * page_size
    history_list = [{
        **news.__dict__,
        "history_id": history_id,
        "view_time": view_time,
    } for news, history_id, view_time in history]
    data = HistoryListResponse(list=history_list, total=total, hasMore=hasmore)
    return success_response(message="获取成功", data=data)
