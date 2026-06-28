#创建users模块化路由
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_config

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@users_router.post("/register")
async def post_register(user_data,db: AsyncSession = Depends(db_config.get_db)):  #用户信息，db
    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "bio": "这个人很懒，什么都没留下",
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
  }
}

