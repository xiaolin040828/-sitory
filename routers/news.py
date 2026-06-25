
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
        page_size: int = Query(default=10, alias="pageSize",le= 100),
):
    return {
        'code': 200,
        'msg': "success",
        "data": {
            "list": '列表',
            "total": "总量",
            "hasMore": "是否更多"
                }
    }


