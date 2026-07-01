from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict


class NewsCategory(BaseModel):
    id: int = Field(description="分类ID")
    name: str = Field(description="分类名称")
    sort_order: int = Field(alias="sortOrder", description="排序顺序")
    create_at: str = Field(alias="createdAt", description="创建时间")
    update_at: str = Field(alias="updateAt", description="更新时间")


class News(BaseModel):
    id: int = Field(..., description="新闻ID")
    title: str = Field(..., description="新闻标题")
    content: str = Field(..., description="新闻内容")
    category: Optional[int] = Field(None, description="分类")
    image: Optional[str] = Field(None, description="新闻图片")
    author: Optional[str] = Field(None, description="新闻作者")
    publish_time: str = Field(alias="publishTime", description="发布时间")
    category_id: int = Field(description="分类ID")
    views: int = Field(description="阅读量")
    created_at: Optional[str] = Field(alias="createdAt", description="创建时间")
    updated_at: Optional[str] = Field(alias="updateAt", description="更新时间")
