from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favourite
from models.users import User
from schemas.favourite import FavouriteResponse, FavouriteStatus
from schemas.common import ApiResponse
from utils.response import success_response  # 导入ApiResponse模型,通用的响应体模型
from utils import auth


router = APIRouter(prefix="/api/favourite", tags=["favourite"])


@router.get("/check", response_model=ApiResponse[FavouriteStatus])
async def check_favourite(news_id: int = Query(..., alias="newsId", description="新闻ID"), current_user: User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    # 先要看是否授权,没有授权,直接返回False

    status: bool = await favourite.check_favourite(db, news_id, current_user.id)
    return success_response(msg="检查收藏状态成功", data=FavouriteStatus(isFavorite=status))


@router.post("/add", response_model=ApiResponse[FavouriteResponse])
async def add_favourite(news_id: int = Query(..., alias="newsId", description="新闻ID"), current_user: User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):

    new_favourite, status = await favourite.add_favourite(db, news_id, current_user.id)
    msg = "添加收藏成功" if status else "已收藏"

    return success_response(msg=msg, data=new_favourite)
