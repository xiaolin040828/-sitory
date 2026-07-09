#新闻相关的缓存-》先读取，后写入
from typing import List, Dict, Any, Optional

from config.cache_config import get_json_cache, set_cache

#缓存的数据key：values
CATEGORY_key = "news:category"
CATEGORY_NEWS_list_key = "news:list"

#查询和新闻分类缓存
async def get_cache_category():
    return await get_json_cache(CATEGORY_key)


#写入新闻分类缓存
async def set_cache_category(date: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORY_key, date, expire)


#写入新闻列表缓存：key = new_list: 分页id： 页码： 每页数量 + 列表数据 + 过去时间
async def set_cache_news_list(categories_id: Optional[int], page: int, page_size: int, new_list: List[Dict[str, Any]], expire: int = 1800, ):
    #调用封装 Redis方法，把新闻列表缓存
    categories_part = categories_id if categories_id is not None else "all"
    key = f"{CATEGORY_NEWS_list_key}{categories_part}:{page}:{page_size}"
    return await set_cache(key=key,value=new_list, expire=expire )

#读取新闻列表
async def get_cache_news_list(categories_id: Optional[int], page: int, page_size: int):
    categories_part = categories_id if categories_id is not None else "all"
    key = f"{CATEGORY_NEWS_list_key}{categories_part}:{page}:{page_size}"
    return await get_json_cache(key=key)


