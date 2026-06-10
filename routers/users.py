from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from models.news import Category, News
from config.db_conf import get_db
from fastapi import Query
from models.news import News
from config.db_conf import get_db
from fastapi import HTTPException
from schemas.users import userregister

router = APIRouter(prefix="/api/user", tags=["user"])




@router.post("/register")
async def register( userdata: userregister, db: AsyncSession = Depends(get_db)):
    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": userdata.username,
      "bio": "这个人很懒，什么都没留下",
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
  }
}