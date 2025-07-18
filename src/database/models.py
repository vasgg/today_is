from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    firstname: Mapped[str | None]
    lastname: Mapped[str | None]
    username: Mapped[str | None] = mapped_column(String(32))
    language_code: Mapped[str | None]
    utc_offset: Mapped[int | None]

    def __str__(self):
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.firstname})"

    def __repr__(self):
        return str(self)


class Record(Base):
    __tablename__ = "records"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    event_name: Mapped[str | None] = mapped_column(String(4096))
    event_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
