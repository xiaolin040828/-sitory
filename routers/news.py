from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_config
from crud import news


news_router = APIRouter(prefix= "/api/router", tags=["news"])



#接口实现流程
#模块化路由-》参照API接口规范文档
#定义数据库，表结构 ——〉参照数据库设计文档
#定义crud函数，封装到crud表
#路由调用crud方法
@news_router.get('/categories')
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession= Depends(db_config.get_db)):
    #调用crud方法
    x = await news.get_categories(db, skip, limit)
    return {
        'code': 200,
        'mag': '类别获取成功',
        'data': x
    }


