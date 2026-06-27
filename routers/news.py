
from fastapi import APIRouter, Depends, Query


from sqlalchemy.ext.asyncio import AsyncSession

from config import db_config
from crud import news

news_router = APIRouter(prefix="/api/news", tags=["news"])


#接口实现流程
#模块化路由-》参照API接口规范文档
#定义数据库，表结构 ——〉参照数据库设计文档
#定义crud函数，封装到crud表
#路由调用crud方法
@news_router.get('/categories')
async def get_new_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db_config.get_db)):
    #调用crud方法
    x = await news.get_categories(db, skip, limit)
    return {
        'code': 200,
        'mag': '类别获取成功',
        'data': x
    }

@news_router.get("/list")
async def get_new_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(default=10, alias="pageSize",le= 10),
        db: AsyncSession = Depends(db_config.get_db)
):
    skip = (page - 1) * page_size
    new_list= await news.get_news(db, category_id, skip, page_size)
    #总量
    total = await news.get_news_count(db, category_id, skip, page_size)
    #查has_more 跳过的数量+当前页的数量是否小于总量
    has_more =  (skip + len(new_list)) > total
    return {
        'code': 200,
        'msg': "success",
        "data": {
            "list": new_list,
            "total": total,
            "hasMore": has_more
                }
    }


@news_router.get("/detail")
async def get_news_detail(
        detail_id: int = Query(..., alias="新闻ID"),
        db: AsyncSession = Depends(db_config.get_db)
):
    return {
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "新闻标题",
    "content": "新闻内容",
    "image": 'null',
    "author": 'null',
    "publishTime": "2023-01-01T00:00:00",
    "categoryId": 1,
    "views": 1,
    "relatedNews": []
  }
}



