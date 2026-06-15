from crud import users
from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(token: str = Header(...), db: AsyncSession = Depends(get_db)):
    # 检查token是否存在
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token无效或过期")  # 401 未授权
    return user
