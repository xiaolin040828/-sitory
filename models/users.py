
from typing import Optional
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Index, Enum
from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped [int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="ID")
    username: Mapped[str] = mapped_column(String(255), nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(255), comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255),  comment="头像URL")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), comment="性别")
    bio: Mapped[Optional[str]] =mapped_column(String(500), comment="个人简介", default="没有简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment="更新时间")




























