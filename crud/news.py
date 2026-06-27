#创建新闻分页列表增删改查的方法

from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select, func
from models import news
from models.news import News


#查新闻分页列表
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_categories = select(news.Category).offset(skip).limit(limit)
    result = await db.execute(db_categories)
    return result.scalars().all()


#查新闻详情
async def get_news(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    db_news = select(news.News).where(news.News.category_id == category_id).offset(skip).limit(limit)
    result = await  db.execute(db_news)
    return result.scalars().all()

#查询指定分类新闻总量
async def get_news_count(db: AsyncSession,category_id, skip: int = 0, limit: int = 10 ):
    db_news = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(db_news)
    return result.scalar_one_or_none()

#获取新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
