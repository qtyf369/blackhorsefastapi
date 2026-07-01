# 新闻缓存方法
from config import cache_conf
from redis import Redis
from typing import Dict
from typing import Any
CATEGORY_KEY = "news:categories"

# 读取新闻分类缓存


async def get_cache_categories():
    return await cache_conf.get_list_dict_cache(CATEGORY_KEY)


# 写入新闻分类缓存
async def set_cache_categories(data: list[Dict[str, Any]]):
    await cache_conf.set_cache(CATEGORY_KEY, data, 7200)


# 缓存新闻列表
NEWS_LIST_KEY = "news:list"
# 读取新闻列表缓存


async def get_cache_news_list():
    return await cache_conf.get_list_dict_cache(NEWS_LIST_KEY)
# 写入新闻列表缓存


async def set_cache_news_list(data: Dict[str, Any]):
    await cache_conf.set_cache(NEWS_LIST_KEY, data, 7200)
