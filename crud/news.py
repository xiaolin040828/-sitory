#创建新闻分页列表增删改查的方法

from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select
from models import news

#查新闻分页列表
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_categories = select(news.Category).offset(skip).limit(limit)
    result = await db.execute(db_categories)
    return result.scalars().all()




