from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),  comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(),  comment="更新时间")


class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序顺序")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order}>"
