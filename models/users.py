from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Index, Enum as SqlalchemyEnum
from typing import Optional
from enum import Enum
from datetime import timezone, datetime, timedelta
from models.base import Base



class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"





class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        Index("idx_user_username", "username"),
        Index("idx_user_phone", "phone"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, comment="用户ID")
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="密码")
    nickname: Mapped[str] = mapped_column(
        String(50), nullable=True, comment="昵称")
    gender: Mapped[str] = mapped_column(SqlalchemyEnum(
        Gender, default=Gender.MALE), nullable=True, comment="性别")
    avatar: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="头像URL")
    bio: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="个人简介")
    phone: Mapped[str] = mapped_column(
        String(20), nullable=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),  comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(),  comment="更新时间")


class Usertoken(Base):
    __tablename__ = "user_token"
    id: Mapped[int] = mapped_column(primary_key=True, comment="用户令牌ID")
    user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="访问令牌")
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)+timedelta(days=7), comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), comment="创建时间")
