#定义数据库类型，定义数据库crud方法（封装）-》路由调用返回
from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#定义基类
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        onupdate= datetime.now,
        comment= "更新时间"
    )
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

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name} sort_order={self.sort_order}>"

