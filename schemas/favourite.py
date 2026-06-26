from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from schemas.base import NewsBase


class FavouriteStatus(BaseModel):
    is_favorite: bool = Field(
        default=False, alias="isFavorite", description="是否收藏")

    model_config = ConfigDict(populate_by_name=True)


class FavouriteResponse(BaseModel):
    id:  int
    user_id: int
    news_id: int
    created_at: datetime


class FavouriteListItem(NewsBase):

    favorite_time: datetime = Field(...,
                                    alias="favoriteTime", description="收藏时间")
    model_config = ConfigDict(populate_by_name=True)


class CheckFavouriteRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class FavouriteListResponse(BaseModel):
    total: int
    list: list[FavouriteListItem]
    has_more: bool = True
