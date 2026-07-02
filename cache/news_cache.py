# 新闻缓存方法
from typing import Optional
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
NEWS_LIST_KEY_PREFIX = "news:list"
# 读取新闻列表缓存


async def get_cache_news_list(category_id: int, page: int, page_size: int):
    key = f"{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{page_size}"
    return await cache_conf.get_list_dict_cache(key)
# 写入新闻列表缓存


async def set_cache_news_list(category_id: Optional[int], data: Dict[str, Any], page: int, page_size: int):
    if category_id is None:
        category_id = 'all'
    key = f"{NEWS_LIST_KEY_PREFIX}:{category_id}:{page}:{page_size}"
    await cache_conf.set_cache(key, data, 1800)


# 缓存新闻详情
NEWS_DETAIL_KEY_PREFIX = "news:detail"
NEWS_RELATED_KEY_PREFIX = "news:related"

# 读取新闻详情缓存


async def get_cache_news_detail(news_id: int):
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    return await cache_conf.get_list_dict_cache(key)

# 写入新闻详情缓存


async def set_cache_news_detail(news_id: int, data: Dict[str, Any]):
    key = f"{NEWS_DETAIL_KEY_PREFIX}:{news_id}"
    await cache_conf.set_cache(key, data, 1800)

# 读取相关新闻缓存


async def get_cache_related_news(news_id: int, category_id: int, limit: int = 5):
    key = f"{NEWS_RELATED_KEY_PREFIX}:{news_id}:{category_id}:{limit}"
    return await cache_conf.get_list_dict_cache(key)

    # 写入相关新闻缓存


async def set_cache_related_news(news_id: int, category_id: int, data: list[Dict[str, Any]], limit: int = 5):
    key = f"{NEWS_RELATED_KEY_PREFIX}:{news_id}:{category_id}:{limit}"
    await cache_conf.set_cache(key, data, 1800)
