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


class History(Base):
    __tablename__ = "history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id"))
    view_time: Mapped[datetime] = mapped_column(
        default=func.now())
