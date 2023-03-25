from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id: int = Field(primary_key=True, unique=True)
    user_id: int = Field(unique=True)
    firstname: Optional[str]
    lastname: Optional[str]
    username: Optional[str]
    created_at: datetime
    updated_at: datetime
    language_code: Optional[str]
    utc_offset: Optional[int]


class Record(SQLModel, table=True):
    __tablename__ = 'records'
    __table_args__ = {'extend_existing': True}
    id: int = Field(primary_key=True, unique=True)
    user_id: int = Field(foreign_key='users.user_id')
    created_at: datetime
    updated_at: datetime
    event_name: str = Field(4096)
    event_date: datetime

