
from sqlalchemy import select, Delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


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
        user_id: int,
        news_id: int
):
    favorite_add = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite_add)
    await db.commit()
    await db.refresh(favorite_add)
    return favorite_add

#取消收藏
async def delete_favorite(db: AsyncSession, news_id: int, user_id: int):
    orm = Delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(orm)
    await db.commit()
    return result.rowcount > 0


#获取收藏列表
async def get_favorite(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    #总量，收藏的欣慰列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    result_count =await db.execute(count_query) #执行获取总量语句
    total = result_count.scalar_one_or_none()
    offset = (page - 1) * page_size
    #获取新闻列表， jion查询+时间排序+分页
    query = (select(News, Favorite.id.label("favorite_id"), Favorite.created_at.label("favorite_time"))
              .join(Favorite, Favorite.news_id == News.id)
              .where(Favorite.user_id == user_id)
              .order_by(Favorite.created_at.desc())
              .offset(offset)
              .limit(page_size)
              )

    result = await db.execute(query)
    rows = result.all()# 元祖类型
    return rows, total

#清空收藏列表
async def clear_favorite(db: AsyncSession, user_id: int, ):
    query = Delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount



