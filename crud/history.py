from sqlalchemy import select, func, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History
from models.news import News


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

#获取浏览列表
async def get_history(
        page: int ,
        page_size: int,
        db: AsyncSession,
        user_id: int,
):
    count_history = select(func.count()).where(History.user_id == user_id)
    result_count = await db.execute(count_history)
    total = result_count.scalar_one_or_none()
    offset = (page - 1) * page_size
    query = (select(News, History.id.label("history_id"),History.view_time.label("view_time"))
             .join(History, History.news_id == News.id)
             .where(History.user_id == user_id)
             .offset(offset)
             .limit(page_size))
    history = await db.execute(query)
    history = history.all()
    return history, total

#删除单条历史记录功能
async def delete_history(
        user_id: int,
        history_id: int,
        db: AsyncSession,
):
    history_delete = Delete(History).where(History.user_id == user_id, History.id == history_id)
    result = await db.execute(history_delete)
    await db.commit()
    return result.rowcount


async def clear_history(
        user_id: int,
        db: AsyncSession,
):
    history_delete = Delete(History).where(History.user_id == user_id)
    result = await db.execute(history_delete)
    await db.commit()
    return result.rowcount