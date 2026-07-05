from datetime import datetime
from sqlalchemy import Integer, DateTime,Index
from sqlalchemy.orm import Mapped, mapped_column
from models.users import Base
from sqlalchemy import ForeignKey

class History(Base):
    __tablename__ = "history"

    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, comment="User ID")
    news_id: Mapped[int] = mapped_column(Integer,ForeignKey("news.id"), nullable=False,comment="New ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,nullable=False,comment="浏览时间")

    def __repr__(self):
        return (f"<History(id={self.id},"
                f" user_id={self.user_id},"
                f" news_id={self.news_id},"
                f" view_time={self.view_time})>"
                )