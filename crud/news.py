from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.news import Category, News
from sqlalchemy import func
from sqlalchemy import and_
from cache.news_cache import get_cache_news_detail, set_cache_news_detail
from cache.news_cache import get_cache_categories, set_cache_categories
from fastapi.encoders import jsonable_encoder
from cache.news_cache import get_cache_news_list, set_cache_news_list
from cache.news_cache import get_cache_related_news, set_cache_related_news
from typing import Optional

# 在crud中直接处理缓存


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先读取缓存，如果没有缓存，再从数据库读取，并设置缓存
    cache_categories = await get_cache_categories()  # 以后把缓存部分逻辑抽离出来，crud中只负责业务逻辑。
    if cache_categories:
        return cache_categories
    # 如果没有缓存，从数据库读取分类缓存
    categories = (await db.execute(select(Category).offset(skip).limit(limit))).scalars().all()
    # 缓存分类
    categories = jsonable_encoder(categories)  # 转换为jsonable格式,把ORM对象转换为字典
    await set_cache_categories(categories)
    return categories


async def get_news_list(db: AsyncSession, category_id: int, page: int = 1, page_size: int = 10):
    # 先读取缓存，如果没有缓存，再从数据库读取，并设置缓存
    # 以后把缓存部分逻辑抽离出来，crud中只负责业务逻辑。
    cache_news_list = await get_cache_news_list(category_id, page, page_size)
    if cache_news_list:
        return cache_news_list

    total = (await db.execute(select(func.count(News.id)).where(News.category_id == category_id))).scalar_one()

    news: list[News] = (await db.execute(select(News).where(News.category_id == category_id).offset((page - 1) * page_size).limit(page_size))).scalars().all()
    has_more: bool = (page - 1) * page_size < total
    news = jsonable_encoder(news)
    # 缓存新闻列表
    await set_cache_news_list(category_id, {'list': news, 'total': total, 'has_more': has_more}, page, page_size)
    return {'list': news, 'total': total, 'has_more': has_more}


async def get_news_detail(db: AsyncSession, id: int):
    # 先读取缓存，如果没有缓存，再从数据库读取，并设置缓存
    # 以后把缓存部分逻辑抽离出来，crud中只负责业务逻辑。
    cache_news_detail = await get_cache_news_detail(id)
    if cache_news_detail:
        return cache_news_detail

    # ORM对象
    result = (await db.execute(select(News).where(News.id == id))).scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    # 缓存新闻详情
    await set_cache_news_detail(id, jsonable_encoder(result))
    return result


async def increase_news_views(db: AsyncSession, id: int):
    result = await db.execute(update(News).where(News.id == id).values(views=News.views + 1))
    return result.rowcount > 0


async def related_news(db: AsyncSession, id: int, category_id: int, limit: int = 5):
    # 先读取缓存，如果没有缓存，再从数据库读取，并设置缓存
    # 以后把缓存部分逻辑抽离出来，crud中只负责业务逻辑。
    cache_related_news = await get_cache_related_news(id, category_id, limit)
    if cache_related_news:
        return cache_related_news

    result = await db.execute(select(News).where(
        and_(News.id != id,
             News.category_id == category_id)).order_by(News.views.desc(), News.publish_time.desc()).limit(limit))
    result = result.scalars().all()
    result = jsonable_encoder(result)
    # 转换为jsonable格式,把ORM对象转换为字典，这就是个列表套字典的格式
    # 缓存相关新闻
    await set_cache_related_news(id, category_id, result, limit)

    if not result:
        return []
    return [{"id": news_detail.id,
             "title": news_detail.title,
             "content": news_detail.content,
             "image": news_detail.image,
             "author": news_detail.author,
             "publishTime": news_detail.publish_time,
             "categoryId": news_detail.category_id,
            "views": news_detail.views, } for news_detail in result]
