from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from fastapi import Query

from utils.response import success_response
from schemas.favourite import FavouriteResponse, FavouriteStatus



router = APIRouter(prefix="/api/favourite", tags=["favourite"])

@router.get("/check", response_model=FavouriteResponse)
async def check_favourite(news_id: int=Query(...,alias="newsId",description="新闻ID"), db: AsyncSession = Depends(get_db)):
    return success_response(data)
