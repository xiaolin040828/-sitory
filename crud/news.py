#创建新闻分页列表增删改查的方法
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select, func, update, values

from cache.news_cache import get_cache_category, set_cache_category, get_cache_news_list, set_cache_news_list
from models import news
from models.news import News, Category
from schemas.base import NewsItemBase


#查新闻分页列表
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    #先从缓存中获取数据
    cashed = await get_cache_category()
    if cashed:
        return cashed

    db_categories = select(news.Category).offset(skip).limit(limit)
    result = await db.execute(db_categories)
    categories = result.scalars().all()

    #写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_category(date=categories)

        return categories

#查新闻列表
async def get_news(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    #读取缓存
    page = skip//limit + 1
    cashed = await get_cache_news_list(categories_id=category_id, page= page , page_size=limit)
    if cashed:
        return [News(**item) for item in cashed]
    db_news = select(news.News).where(news.News.category_id == category_id).offset(skip).limit(limit)
    result = await  db.execute(db_news)
    news_list = result.scalars().all()

    #写入缓存
    if news_list:
        #先把orm对象转成字典
        #先把orm转pydantic再转字典
        news_date_list = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(categories_id=category_id, new_list= news_date_list, page= page, page_size=limit)

    return news_list


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

#浏览功能-------更改数据库的浏览量字段的数值
async def update_news_views(db: AsyncSession, new_id: int):
    stmt = update(News).where(News.id == new_id).values(views = News.views + 1)
    await db.execute(stmt)
    await db.commit()


#获取相关类型的新闻
async def get_relatedNews(db: AsyncSession, news_id: int, category_id : int ,limit: int = 5):
    stmt = select(News).where(News.id !=news_id, News.category_id == category_id).order_by(News.views.desc()).limit(limit)
    result = await db.execute(stmt)
    return  result.scalars().all()
    #列表推导式
    # values = result.scalars().all()
    # return [{
    #     "id": i.id,
    #     "title": i.title,
    #     "content": i.content,
    #     "image": i.image,
    #     "author": i.author,
    #     "publishTime": i.publishTime,
    #     "categoryId": i.category_id,
    #     "views": i.views,
    # }for i in values]



