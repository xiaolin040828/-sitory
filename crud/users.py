from sqlalchemy import select
from schemas.users import UserRequest
from models.users import User
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
