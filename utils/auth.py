#整合根据token查询用户最后返回用户
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users

async def get_current_use(
        authorizationr: str = Header(..., alias= "Authorization"),
        db: AsyncSession = Depends(get_db)):
    token = authorizationr.replace("Bearer ", "")
    user = users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌")
    return user
