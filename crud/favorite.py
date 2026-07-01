
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite


#检查收藏状态：当前用户是否收藏了这条新闻
async def is_new_favorite(
        user_id,
        news_id,
        db: AsyncSession,
):
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None
