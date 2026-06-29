import redis.asyncio as redis
import json
redis_client = redis.from_url('redis://localhost:6379/0',decode_responses=True)

# 缓存配置, 缓存过期时间
CACHE_EXPIRE = 60 * 5

#读取字符串
async def get_str(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"读取字符串失败: {e}")
        return None
#读取列表或字典
async def get_list_dict(key: str):
    try:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"读取列表或字典失败: {e}")
        return None


# 写入字符串
async def set_str(key: str, value: str, expire: int = CACHE_EXPIRE):
    await redis_client.setex(key, expire, value)