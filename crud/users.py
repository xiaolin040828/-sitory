from sqlalchemy import select
from schemas.users import UserRequest
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

#根据用户名获取用户数据
async def get_users_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

#创建用户
async  def create_user(db: AsyncSession, user_data: UserRequest):
    pass
