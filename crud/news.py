from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.news import Category, News
from sqlalchemy import func
from sqlalchemy import and_


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):

    return (await db.execute(select(Category).offset(skip).limit(limit))).scalars().all()


async def get_news_list(db: AsyncSession, category_id: int, page: int = 1, page_size: int = 10):
    total = (await db.execute(select(func.count(News.id)).where(News.category_id == category_id))).scalar_one()

    news: list[News] = (await db.execute(select(News).where(News.category_id == category_id).offset((page - 1) * page_size).limit(page_size))).scalars().all()
    has_more: bool = (page - 1) * page_size < total
    return {'list': news, 'total': total, 'has_more': has_more}


async def get_news_detail(db: AsyncSession, id: int):
    result = (await db.execute(select(News).where(News.id == id))).scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result


async def increase_news_views(db: AsyncSession, id: int):
    result = await db.execute(update(News).where(News.id == id).values(views=News.views + 1))
    return result.rowcount > 0


async def related_news(db: AsyncSession, id: int, category_id: int, limit: int = 5):
    result = await db.execute(select(News).where(
        and_(News.id != id,
             News.category_id == category_id)).order_by(News.views.desc(), News.publish_time.desc()).limit(limit))
    result = result.scalars().all()

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
