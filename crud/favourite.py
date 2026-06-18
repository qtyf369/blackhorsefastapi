from models.favourite import FavourtieNews
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


async def check_favourite(db: AsyncSession, news_id: int, user_id: int) -> bool:
    result = await db.execute(select(FavourtieNews).where(FavourtieNews.news_id == news_id, FavourtieNews.user_id == user_id))
    return result.scalar_one_or_none() is not None

# 添加收藏


async def add_favourite(db: AsyncSession, news_id: int, user_id: int):
    # 先检查是否收藏过，如果已收藏，直接返回已收藏的记录
    stmt = select(FavourtieNews).where(FavourtieNews.news_id ==
                                       news_id, FavourtieNews.user_id == user_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing is not None:
        return existing, False

    new_favourite = FavourtieNews(news_id=news_id, user_id=user_id)
    db.add(new_favourite)
    # 数据库里有created_at字段,需要刷新才能获取到正确的值
    await db.flush()
    await db.refresh(new_favourite)
    return new_favourite, True
