from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from utils import auth
from schemas.common import ApiResponse
from fastapi import Query

from crud import history
from schemas.history import HistoryAddResponse, HistoryListResponse, HistoryRequest, HistoryDetailResponse
from models.history import History
from utils.response import success_response
from fastapi import HTTPException


router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add", response_model=ApiResponse[HistoryAddResponse])
async def add_history(request: HistoryRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth.get_current_user)):

    result = await history.add_history(db, request.news_id, current_user.id)
    data = HistoryAddResponse.model_validate(result)
    return success_response(msg="添加成功", data=data)


@router.get("/list", response_model=ApiResponse[HistoryListResponse])
async def get_history_list(db: AsyncSession = Depends(get_db), current_user: User = Depends(auth.get_current_user), page: int = Query(1, description="页码"), page_size: int = Query(10, alias="pageSize", description="每页数量")):
    rows, total, has_more = await history.get_history_list(db, current_user.id, page, page_size)
    list = []
    for item, view_time in rows:
        listitem = HistoryDetailResponse.model_validate(item)
        listitem.view_time = view_time
        list.append(listitem)
    response = HistoryListResponse(
        total=total, has_more=has_more, items=list)
    return success_response(msg="查询成功", data=response)


@router.delete("/delete/{history_id}", response_model=ApiResponse[None])
async def delete_history(history_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    status = await history.delete_history(db, history_id, current_user.id)
    if not status:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    return success_response(msg="删除成功", data=None)


@router.delete("/clear", response_model=ApiResponse[None])
async def clear_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    status = await history.clear_history(db, current_user.id)
    if not status:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    return success_response(msg="清空成功", data=None)
