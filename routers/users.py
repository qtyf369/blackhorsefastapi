from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import users
from config.db_conf import get_db
from fastapi import HTTPException, status
from schemas.users import userInfoBase, userInfoResponse, userregister, userAuthResponse
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register", response_model=userAuthResponse)
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
    data = userAuthResponse(token=user_token, userInfo=userInfoResponse.model_validate(
        user))  # model_validate 将ORM模型转换为userInfoBase模型
    return success_response(msg="注册成功", data=data)
    # 返回注册成功响应
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": user_token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar
    #         }
    #     }
    # }
