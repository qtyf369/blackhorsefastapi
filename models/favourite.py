from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Index
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.news import News
from models.base import Base






class FavourtieNews(Base):
    __tablename__ = "favourite"
    id: Mapped[int] = mapped_column(Integer,  primary_key=True, comment="收藏id")
    user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="用户id")
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("news.id"), nullable=False, comment="新闻id")
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), comment="创建时间")
    news: Mapped["News"] = relationship(News) # 关联新闻模型
