from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str

class Userinfo(BaseModel):
    nickname: Optional[str] = Field(default=None, max_length=150, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserinfoResponse(Userinfo):
    id : int
    username : str

    model_config = ConfigDict(
        from_attributes=True #允许 Pydantic 从“对象属性（ORM模型）”读取数据
    )


class UserAuthResponse(BaseModel):
    token: str
    userinfo: Userinfo = Field(..., alias="userInfo")
    #模型配置
    model_config = ConfigDict(
         populate_by_name=True,
         from_attributes=True) #alias 和字段名“双通道兼容”
