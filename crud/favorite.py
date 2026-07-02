
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from models.favorite import Favorite
from schemas.favorite import Favorite_userid


#检查收藏状态：当前用户是否收藏了这条新闻
async def is_new_favorite(
        user_id,
        news_id,
        db: AsyncSession,
):
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


#添加收藏
async def add_favorite(
        db: AsyncSession,
        user_id,
        news_id
):
    favorite_add = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite_add)
    await db.commit()
    await db.refresh(favorite_add)
    return favorite_add

#取消收藏
async def delete_favorite(db: AsyncSession, news_id: int, user_id: int):
    orm = update(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(orm)
    await db.commit()
    return result.rowcount > 0
