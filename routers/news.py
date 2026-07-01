from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from models.news import Category, News
from fastapi import Query
from models.news import News
from config.db_conf import get_db
from fastapi import HTTPException
from schemas.common import ApiResponse
from schemas.news import NewsCategory
from utils.response import success_response
router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories", response_model=ApiResponse[list[NewsCategory]])
async def get_categories(
        db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):

    # 从数据库获取新闻分类列表,这是Python对象
    categories = await news.get_categories(db, skip, limit)
    # 转换为Pydantic模型
    categories = [NewsCategory.model_validate(
        category) for category in categories]
    return success_response(msg="success", data=categories)


@router.get("/list")
async def get_news_list(
        db: AsyncSession = Depends(get_db),
        category_id: int = Query(..., alias="categoryId"),
        page: int = Query(default=1, alias="page"),
        page_size: int = Query(default=10, alias="pageSize")):
    news_data = await news.get_news_list(db, category_id, page, page_size)
    newslist: list[News] = news_data['list']
    total: int = news_data['total']
    has_more: bool = news_data['has_more']
    return {
        "code": 200,
        "message": "success",
        "data": {'list': newslist, 'total': total, 'has_more': has_more}
    }


@router.get("/detail", response_model=ApiResponse[News])
async def get_news_detail(
        db: AsyncSession = Depends(get_db),
        id: int = Query(..., alias="id")):
    news_detail = await news.get_news_detail(db, id)

    # 增加views 并返回是否成功
    success: bool = await news.increase_news_views(db, id)
    if not success:  # 命中检测
        raise HTTPException(status_code=400, detail="Views increase failed")

    # 获取相关新闻
    related_news: list[News] = await news.related_news(db, id, news_detail.category_id)

    return success_response(msg="success", data={
        "id": id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
        "relatedNews": related_news
    })
