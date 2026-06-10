from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Index
from typing import Optional


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),  comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(),  comment="更新时间")


# 新闻类别模型
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序顺序")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order}>"

# 新闻模型


class News(Base):
    __tablename__ = "news"

    __table_args__ = (
        Index("idx_news_category_id", "category_id"),
        Index("idx_news_publish_time", "publish_time")
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="新闻描述")
    content: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="新闻图片URL")
    author: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="作者")
    category_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="分类ID")

    views: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="点击量")
    publish_time: Mapped[datetime] = mapped_column(DateTime,
                                                   default=func.now(),  comment="发布时间时间")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, category_id={self.category_id}, views={self.views}>"
