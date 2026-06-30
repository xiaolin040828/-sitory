import uuid
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy import select

from config.db_config import get_db
from schemas.users import UserRequest
from models.users import User, UserToken
from sqlalchemy.ext.asyncio import AsyncSession
from utils.securty import get_password_hash, verify_password

#根据用户名获取用户数据
async def get_users_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

#创建用户
async  def create_user(db: AsyncSession, user_data: UserRequest):
    #注册逻辑：查询数据库是否有同账号-》创建用户-〉生成token-》响应结果
    psw_hash = get_password_hash(user_data.password)
    user = User(username=user_data.username, password=psw_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

#生成token
async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())   #通过uuid方法生成token转字符串
    #token时间= 创建时间+ 7days
    expirse = datetime.now() + timedelta(days= 7)
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(stmt)
    user_token = result.scalars().first()
    if user_token: #如过有token就更新时间
        user_token.token = token
        user_token.expires_at = expirse
    else:   #如果没有就添加新的token到db
        user_token = UserToken(user_id = user_id, token = token, expires_at = expirse)
        db.add(user_token)
        await db.commit()

    return token

#验证用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_users_username(db, username)      #通过上面定义的获取用户
    if not user:
        return None
    if not verify_password(plain_password= password, hashed_password= user.password):
        return None

    return user


#根据token查询用户: 验证token -> 查询用户
#整合了根据token查询用户并且判断token是否过期，查询用户信息
async def get_user_by_token(token: str, db: AsyncSession):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#修改用户信息
async def update_current_user(db: AsyncSession):
    