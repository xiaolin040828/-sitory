#封装缓存方法

import json
from typing import Any

import redis.asyncio as redis

RIDES_port = 6379
RIDES_host = "localhost"
RIDES_db = 0

redis_client = redis.Redis(host=RIDES_host,
                    port=RIDES_port,
                    db=RIDES_db,
                    decode_responses=True)

#缓存的方法设置缓存“set“传参传key，values， expire“缓存时间“，获取缓存“get“传参传key
#读取 和 设置 缓存
#获取字符串
async def get_cache(key: str):
    try:
        return redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败{e}")
        return None

#获取字典，或者列表
async def get_json_cache(key: str):
    try:
        date = await redis_client.get(key)
        if date:
            return json.loads(date)
        return None
    except Exception as e:
        print(f"获取JSON缓存失败{e}")
        return None

#设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (list, dict)):
            #转字符串再寸
            value = json.dumps(value, ensure_ascii=False) #中文不转义
        await redis_client.set(key, value, ex=expire)
        return True
    except Exception as e:
        print(f"设置缓存失败{e}")
        return False





