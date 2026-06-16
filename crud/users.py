from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.news import Category, News
from sqlalchemy import func
from sqlalchemy import and_
from models.users import User, Usertoken
from schemas.users import UserUpdateRequest, userregister
import uuid
from datetime import datetime, timedelta, timezone


async def get_user_by_username(db: AsyncSession, username: str):
    user = await db.execute(select(User).where(User.username == username))
    return user.scalar_one_or_none()


async def create_user(db: AsyncSession, userdata: userregister):
    from utils.security import hash_password
    encrypted_password = hash_password(userdata.password)
    user = User(
        username=userdata.username,
        password=encrypted_password,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
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

# 根据token查询用户


async def get_user_by_token(db: AsyncSession, token: str):
    result = await db.execute(select(Usertoken).where(Usertoken.token == token))
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return None

    query = await db.execute(select(User).where(User.id == db_token.user_id))
    user = query.scalar_one_or_none()

    return user


async def update_user(db: AsyncSession, username: str, userdata: UserUpdateRequest):
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    for key, value in userdata.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await db.flush()
    await db.refresh(user)  # 这里不需要这两句也没事，return会从内存中拿到新值。
    return user


async def update_password(db: AsyncSession, user: User, new_password: str, old_password: str):

    from utils.security import verify_password
    if not verify_password(old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="旧密码错误")
    from utils.security import hash_password
    new_password = hash_password(new_password)
    user.password = new_password
    await db.flush()
    await db.refresh(user)
    return user
