from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import ForeignKey
from schemas.base import NewsBase


class HistoryAddResponse(BaseModel):
    id: int = Field(..., alias="historyId", description="历史记录ID")
    user_id: int = Field(..., alias="userId", description="用户ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    view_time: datetime = Field(..., alias="viewTime", description="历史记录时间")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryDetailResponse(NewsBase):
    view_time: datetime = Field(
        default=datetime.now, alias="viewTime", description="历史记录时间")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryListResponse(BaseModel):
    total: int = Field(..., description="总记录数")
    has_more: bool = Field(..., description="是否有更多记录")
    items: list[HistoryDetailResponse] = Field(
        ..., alias="list", description="历史记录列表")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
