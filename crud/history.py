from models.favourite import FavourtieNews
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import delete  # 导入删除语句 delete
from sqlalchemy import func  # 导入函数函数 func
from models.history import History
from datetime import datetime

from models.news import News


async def add_history(
    db: AsyncSession, news_id: int, user_id: int
) -> History:
    # 检查是否存在相同的记录记录,有的话，更新时间，没有的话，新增
    stmt = select(History).where(History.user_id ==
                                 user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    exist_history = result.scalars().first()
    if exist_history:
        exist_history.view_time = datetime.now()
        history = exist_history
    else:
        history = History(
            news_id=news_id, user_id=user_id
        )

    db.add(history)
    await db.flush()
    await db.refresh(history)
    return history


async def get_history_list(
    db: AsyncSession, user_id: int, page: int, page_size: int
):
    offset = (page - 1) * page_size
    limit = page_size
    total = (await db.execute(
        select(func.count(History.id)).where(History.user_id == user_id)
    )).scalar_one()
    has_more = offset + limit < total
    stmt = select(News, History.view_time).join(History, News.id == History.news_id).where(
        History.user_id == user_id).offset(offset).limit(limit)

    result = await db.execute(stmt)
    rows = result.all()  # 包含row对象的列表 （新闻对象，历史记录时间）
    return rows, total, has_more


async def delete_history(
        db: AsyncSession, history_id: int, user_id: int):
    stmt = delete(History).where(
        History.news_id == history_id, History.user_id == user_id
    )

    result = await db.execute(stmt)

    return result.rowcount > 0


async def clear_history(
        db: AsyncSession, user_id: int):
    stmt = delete(History).where(
        History.user_id == user_id
    )

    result = await db.execute(stmt)

    return result.rowcount > 0
