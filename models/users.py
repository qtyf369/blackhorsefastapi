from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Index, Enum as SqlalchemyEnum
from typing import Optional
from news import Base
from enum import Enum



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
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    nickname: Mapped[str] = mapped_column(String(50), nullable=True, comment="昵称")
    gender: Mapped[str] = mapped_column(SqlalchemyEnum(Gender, default=Gender.MALE), nullable=True, comment="性别")
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, comment="头像URL")
    bio: Mapped[str] = mapped_column(String(255), nullable=True, comment="个人简介")
    phone: Mapped[str] = mapped_column(String(20), nullable=True, comment="手机号")
