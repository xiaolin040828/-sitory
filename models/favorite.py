from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Favorite(DeclarativeBase):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)