from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User
from config.db_config import get_db
from schemas.history import History_newsid, HistoryAddResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud.history import add_history
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
    return success_response(message="添加成功",data=data)

