#创建users模块化路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config import db_config
from crud.users import get_users_username, create_user, create_token
from schemas.users import UserRequest

user_router = APIRouter(
    prefix="/api/user",
    tags=["users"],
)


@user_router.post("/register")
async def post_register(user_data: UserRequest,db: AsyncSession = Depends(db_config.get_db)): #用户信息，db
    existing_user = await  get_users_username(db= db, username= user_data.username )
    if existing_user:
        raise HTTPException(status_code=400,detail="用户已经存在")
    return_user =  await create_user(db= db, user_data= user_data)
    token = await create_token(db= db, user_id= return_user.id)
    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": token,
    "userInfo": {
      "id": return_user.id,
      "username": return_user.username,
      "bio": return_user.bio,
      "avatar": return_user.avatar,
    }
  }
}

