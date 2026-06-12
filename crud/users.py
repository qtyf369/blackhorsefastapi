from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.news import Category, News
from sqlalchemy import func
from sqlalchemy import and_
from models.users import User, Usertoken
from schemas.users import userregister
import uuid
from datetime import datetime, timedelta, timezone


async def get_user_by_username(db: AsyncSession, username: str):
    user = await db.execute(select(User).where(User.username == username))
    return user.scalar_one_or_none()


async def create_user(db: AsyncSession, userdata: userregister):
    # 不检查用户名是否存在，直接注册，只负责单个功能。用passlib加密密码。但写入数据库时会检查用户名是否存在，捕获后，抛出友好可读的错误信息。不然FastApi会报500错误。
    try:
        from utils.security import hash_password
        encrypted_password = hash_password(userdata.password)
        # 创建用户实例，一开始只需要用户名和密码。给模型类的字段赋值。
        user = User(
            username=userdata.username,
            password=encrypted_password,
        )
        db.add(user)  # 这是个同步操作，会立即执行。把用户实例添加到会话中。会话结束时，会自动提交事务。
        await db.flush()  # 把写入操作提交到数据库，但不会提交事务。
        await db.refresh(user)  # 刷新用户实例，加载其他数据库生成的值。
    except IntegrityError as e:  # 唯一约束冲突
        raise HTTPException(status_code=400, detail="用户名已存在")
    return user


async def create_user_token(db: AsyncSession, user_id: int):

    # 查询是否有TOKEN，有则更新，无则创建
    result = await db.execute(select(Usertoken).where(Usertoken.user_id == user_id))
    old = result.scalar_one_or_none()
    new_token = str(uuid.uuid4())
    new_expires_at = datetime.now(timezone.utc)+timedelta(days=7)

    if old:
        old.token = new_token
        old.expires_at = new_expires_at

    else:
        # 如果有旧的Token，就不需要创建新的，节省内存，把这个创建放在这里。前面用创建字段。
        token = Usertoken(
            user_id=user_id,
            token=new_token,
            expires_at=new_expires_at)
        db.add(token)

    return new_token  # 返回新的Token
