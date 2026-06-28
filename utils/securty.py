from passlib.context import CryptContext

#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#用hash方法吧用户输入的明文转加密
async def get_password_hash(password: str):
    return pwd_context.hash(password)



