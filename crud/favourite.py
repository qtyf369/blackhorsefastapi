from models.favourite import FavourtieNews
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import delete  # 导入删除语句 delete
from sqlalchemy import func  # 导入函数函数 func


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

async def remove_favourite(db: AsyncSession, news_id: int, user_id: int):
    stmt = delete(FavourtieNews).where(FavourtieNews.news_id == news_id, FavourtieNews.user_id == user_id)
    result = await db.execute(stmt)
    return result.rowcount > 0


# 获取收藏列表
async def get_favourite_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    stmt = select(FavourtieNews).where(FavourtieNews.user_id == user_id).order_by(FavourtieNews.id)
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset)
    stmt = stmt.limit(page_size)
    result = await db.execute(stmt) 
    total = await db.execute(select(func.count(FavourtieNews.id)).where(FavourtieNews.user_id == user_id))
    has_more = total.scalar_one_or_none() > offset + page_size
    list = result.scalars().all()
    return FavouriteListResponse(total=total.scalar_one_or_none(), list=list, has_more=has_more)
