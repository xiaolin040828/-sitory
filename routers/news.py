from fastapi import APIRouter

news_router = APIRouter(prefix= "/api/router/", tags=["news"])

@news_router.get('/categories')
async def get_categories():
    return {'mag': '类别获取成功'}

