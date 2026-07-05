#定义数据库类型，定义数据库crud方法（封装）-》路由调用返回
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from models.users import Base
from typing import Optional



#定义基类

#定义模型类
class Category(Base):
    __tablename__ = 'news_category'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment= '分页ID'
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable= False,comment= "分类名")
    sort_order: Mapped[int] = mapped_column(Integer, default= 0, nullable= False,comment= "排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now, comment= "更新时间")

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} sort_order={self.sort_order}>"

#定义新闻模型类
class News(Base):
    __tablename__ = 'news'
    #创建索引，提高查询速度
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),
        Index("idx_publish_time", "publish_time")
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="新闻标题")
    description: Mapped[str] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="新闻图URL" )
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now, comment= "更新时间")

    def __repr__(self):
        return f"<news(id = {self.id}, title='{self.title}', views={self.views})>"
