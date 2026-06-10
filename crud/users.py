from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.news import Category, News
from sqlalchemy import func
from sqlalchemy import and_
from models.users import User
from schemas.users import userregister



async def register_user(userdata: userregister, db: AsyncSession):
    # 检查用户名是否存在
    existing_user = await db.execute(select(User).where(User.username == userdata.username))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="用户名已存在")
