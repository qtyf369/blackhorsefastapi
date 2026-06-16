from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import users
from models.users import User
from schemas.users import (
    ApiResponse,
    UserUpdateRequest,
    UserPasswordUpdateRequest,
    userDataResponse,
    userInfoResponse,
    userregister,
)
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register", response_model=ApiResponse[userDataResponse])
async def register(userdata: userregister, db: AsyncSession = Depends(get_db)):
    # 检查用户名是否存在
    existing_user = await users.get_user_by_username(db, userdata.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    # 注册用户

    user = await users.create_user(db, userdata)  # crud内部已经处理错误

    # 生成访问令牌
    user_token: str = await users.create_user_token(db, user.id)
    data = userDataResponse(token=user_token, userInfo=userInfoResponse.model_validate(
        user))  # model_validate 将ORM模型转换为userInfoBase模型
    return success_response(msg="注册成功", data=data)


@router.post("/login", response_model=ApiResponse[userDataResponse])
async def login(userdata: userregister, db: AsyncSession = Depends(get_db)):
    # 检查用户名是否存在
    existing_user = await users.get_user_by_username(db, userdata.username)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名不存在")
    # 检查密码是否正确
    from utils.security import verify_password
    if not verify_password(userdata.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误")
    # 登录成功
    user_token: str = await users.create_user_token(db, existing_user.id)
    data = userDataResponse(token=user_token, userInfo=userInfoResponse.model_validate(
        existing_user))  # model_validate 将ORM模型转换为userInfoBase模型
    return success_response(msg="登录成功", data=data)


@router.get("/info", response_model=ApiResponse[userInfoResponse])
async def get_info(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    data = userInfoResponse.model_validate(user)
    return success_response(msg="获取用户信息成功", data=data)


@router.put("/update", response_model=ApiResponse[userInfoResponse])
async def update_info(userdata: UserUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # put是文档里的，一般用于更新所有字段，patch是更新指定字段
    # 更新用户信息
    await users.update_user(db, user.username, userdata)
    return success_response(msg="更新用户信息成功", data=userInfoResponse.model_validate(user))


@router.put("/password", response_model=ApiResponse[userInfoResponse])
async def update_password(userdata: UserPasswordUpdateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # 更新用户密码
    await users.update_password(db, user, userdata.new_password, userdata.old_password)
    return success_response(msg="更新用户密码成功", data=userInfoResponse.model_validate(user))
