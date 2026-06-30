from passlib.context import CryptContext

#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#用hash方法吧用户输入的明文转加密
def get_password_hash(password: str):
    return pwd_context.hash(password)

#密码验证
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)      #通过verify方法得到布尔类型


