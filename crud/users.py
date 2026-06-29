import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from schemas.users import UserRequest
from models.users import User, UserToken
from sqlalchemy.ext.asyncio import AsyncSession
from utils.securty import get_password_hash

#根据用户名获取用户数据
async def get_users_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

#创建用户
async  def create_user(db: AsyncSession, user_data: UserRequest):
    #注册逻辑：查询数据库是否有同账号-》创建用户-〉生成token-》响应结果
    psw_hash = await get_password_hash(user_data.password)
    user = User(username=user_data.username, password=psw_hash)
    db.add(user)
    await db.refresh(user)
    await db.commit()
    return user

#生成token
async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())   #通过uuid方法生成token转字符串
    #token时间= 创建时间+ 7days
    expirse = datetime.now() + timedelta(days= 7)
    stmt = select(UserToken).where(User.id == UserToken.user_id)
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
