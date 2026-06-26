from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class NewsBase(BaseModel):
    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    description: Optional[str] = Field(None, description="新闻描述")
    image: Optional[str] = Field(None, description="新闻图片URL")
    author: Optional[str] = Field(None, description="作者")
    publish_time: Optional[datetime] = Field(
        None, alias="publishTime", description="发布时间")
    category_id: Optional[int] = Field(
        None, alias="categoryId", description="分类ID")
    views: Optional[int] = Field(None, description="浏览量")
