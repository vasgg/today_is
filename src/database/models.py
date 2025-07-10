from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, primary_key=True)
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(String(32))

    def __str__(self):
        return f"{self.__class__.__name__}(id: {self.id}, fullname: {self.fullname})"

    def __repr__(self):
        return str(self)
