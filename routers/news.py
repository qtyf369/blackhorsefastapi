from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from models.news import Category
from config.db_conf import get_db
from fastapi import Query
from models.news import News



router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(
        db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db), 
        category_id: int = Query(..., alias="categoryId"),
        page: int = Query(default=1, alias="page"), 
        page_size: int = Query(default=10, alias="pageSize")):
    news_data = await news.get_news(db, category_id, page, page_size)
    newslist: list[News] = news_data['list']
    total: int = news_data['total']
    has_more: bool = news_data['has_more']
    return {
        "code": 200,
        "message": "success",
        "data":{'list': newslist, 'total': total, 'has_more': has_more}
    }