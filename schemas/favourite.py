from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class FavouriteStatus(BaseModel):
    is_favorite: bool = Field( default=False, alias="isFavorite", description="是否收藏")
    
    model_config = ConfigDict(populate_by_name=True)  

class FavouriteResponse(BaseModel):
    id:  int
    user_id: int
    news_id: int
    created_at: datetime




class FavouriteListItem(BaseModel):
    id: int = Field(..., description="收藏ID")
    title: str = Field(..., description="新闻标题")
    description: Optional[str] = Field(None, description="新闻描述")
    image: Optional[str] = Field(None, description="新闻图片URL")
    author: Optional[str] = Field(None, description="作者")
    publish_time: Optional[datetime] = Field(None, alias="publishTime", description="发布时间")
    category_id: Optional[int] = Field(None, alias="categoryId", description="分类ID")
    views: Optional[int] = Field(None, description="浏览量")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")

class CheckFavouriteRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

class FavouriteListResponse(BaseModel):
    total: int
    list: list[FavouriteListItem]
    has_more: bool = True