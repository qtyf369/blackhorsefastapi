from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News
from sqlalchemy import func


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):

    return (await db.execute(select(Category).offset(skip).limit(limit))).scalars().all()


async def get_news_list(db: AsyncSession, category_id: int, page: int = 1, page_size: int = 10):
    total: int = (await db.execute(select(func.count()).where(News.category_id == category_id))).scalar()
    news: list[News] = (await db.execute(select(News).where(News.category_id == category_id).offset((page - 1) * page_size).limit(page_size))).scalars().all()
    has_more: bool = (page - 1) * page_size < total
    return {'list': news, 'total': total, 'has_more': has_more}


async def get_news_detail(db: AsyncSession, id: int):
    result = (await db.execute(select(News).where(News.id == id))).scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result
