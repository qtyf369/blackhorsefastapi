# 新闻缓存方法
from config import cache_conf
from redis import Redis
CATEGORY_KEY = "news:categories"
from typing import Dict
from typing import Any

# 读取新闻分类
async def get_cache_categories():
  return await cache_conf.get_list_dict_cache(CATEGORY_KEY)



# 写入新闻分类
async def set_cache_categories(data: list[Dict[str, Any]]):
  await cache_conf.set_cache(CATEGORY_KEY, data, 600)
