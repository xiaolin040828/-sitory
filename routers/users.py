#创建users模块化路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_config
from crud.users import get_users_username, create_user
from schemas.users import UserRequest

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@users_router.post("/register")
async def post_register(user_data: UserRequest,db: AsyncSession = Depends(db_config.get_db)): #用户信息，db
    existing_user = await  get_users_username(db= db, username= user_data.username )
    if existing_user:
        raise HTTPException(status_code=400,detail="用户已经存在")
    return_user =  await create_user(db= db, user_data= user_data)

    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": return_user.id,
      "username": return_user.username,
      "bio": return_user.bio,
      "avatar": return_user.avatar,
    }
  }
}

