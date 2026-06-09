from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from models.news import Category
from config.db_conf import get_db

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
