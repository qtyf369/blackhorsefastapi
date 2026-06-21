from fastapi import APIRouter, Body, Depends
from fastapi import HTTPException, status
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favourite
from models.users import User
from schemas.favourite import FavouriteListResponse, FavouriteResponse, FavouriteStatus
from schemas.common import ApiResponse
from utils.response import success_response  # 导入ApiResponse模型,通用的响应体模型
from utils import auth
from schemas.favourite import CheckFavouriteRequest


router = APIRouter(prefix="/api/favorite", tags=["favorite"]) #前端取的接口是favorite，我这里就改了。别的还是用favourite


@router.get("/check", response_model=ApiResponse[FavouriteStatus])
async def check_favourite(news_id: int = Query(..., alias="newsId", description="新闻ID"), current_user: User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    # 先要看是否授权,没有授权,直接返回False
  
    status: bool = await favourite.check_favourite(db, news_id, current_user.id)
    return success_response(msg="检查收藏状态成功", data=FavouriteStatus(is_favorite=status))


@router.post("/add", response_model=ApiResponse[FavouriteResponse])
async def add_favourite(request: CheckFavouriteRequest, current_user: User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):

    new_favourite, status = await favourite.add_favourite(db, request.news_id, current_user.id)
    msg = "添加收藏成功" if status else "已收藏"

    return success_response(msg=msg, data=new_favourite)

#取消收藏
@router.delete("/remove", response_model=ApiResponse[None])    
async def remove_favourite(news_id: int = Query(..., alias="newsId", description="新闻ID"), current_user: User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    status = await favourite.remove_favourite(db, news_id, current_user.id)
    if not status:
        raise HTTPException(status_code=404, detail="删除未成功，未收藏")

    
    return success_response(msg="取消收藏成功", data=None)

@router.get("/list", response_model=ApiResponse[FavouriteListResponse])
async def get_favourite_list(current_user: User = Depends(auth.get_current_user),
page: int = Query(1, alias="page", description="页码"),
page_size: int = Query(10, alias="pageSize", le=100, description="每页数量"),
 db: AsyncSession = Depends(get_db)):
    favourites = await favourite.get_favourite_list(db, current_user.id, page, page_size)
    return success_response(msg="获取收藏列表成功", data=favourites)