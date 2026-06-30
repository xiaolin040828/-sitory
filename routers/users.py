#创建users模块化路由
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import db_config
from crud.users import get_users_username, create_user, create_token, authenticate_user
from schemas.users import UserRequest, UserAuthResponse, UserinfoResponse
from utils.response import success_response

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
#     return {
#   "code": 200,
#   "message": "注册成功",
#   "data": {
#     "token": token,
#     "userInfo": {
#       "id": return_user.id,
#       "username": return_user.username,
#       "bio": return_user.bio,
#       "avatar": return_user.avatar,
#     }
#   }
# }

    response_data = UserAuthResponse(token= token, userInfo= UserinfoResponse.model_validate(return_user))
    return success_response(message="success", data=response_data)

#用户登陆路由
@user_router.post("/login")
#登陆逻辑：验证用户账号是否存在-> 验证密码-> 生成token -> 响应结果
async def post_login(user_data: UserRequest, db: AsyncSession = Depends(db_config.get_db)):
    user = await authenticate_user(db= db, username= user_data.username, password= user_data.password)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="用户账号或密码错误")
    token = await create_token(db= db, user_id= user.id)
    response_data = UserAuthResponse(token= token, userInfo= UserinfoResponse.model_validate(user))
    return success_response(message= "success", data= response_data)

#获取用户信息
#封装一个方法查token，查用户)->功能整合成一个工具函数 ->登陆-》获取信息
@user_router.get("/info")
#验证token是否过期
async def get_user_info():
    return success_response(message="success")