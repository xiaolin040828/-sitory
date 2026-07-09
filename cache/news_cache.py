#新闻相关的缓存-》先读取，后写入
from typing import List, Dict, Any

from config.cache_config import get_json_cache, set_cache

#缓存的数据key：values
CATEGORY_key = "news:category"

#查询和新闻列表缓存
async def get_cache_category():
    return await get_json_cache(CATEGORY_key)


#写入新闻列表缓存
async def set_cache_category(date: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORY_key, date, expire)


