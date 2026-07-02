from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History


#添加收藏记录
async def add_history(
        user_id: int,
        news_id: int,
        db: AsyncSession,
):
    history_add = History(user_id=user_id, news_id=news_id)
    db.add(history_add)
    await db.commit()
    await db.refresh(history_add)
    return history_add