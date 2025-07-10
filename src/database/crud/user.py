from aiogram.types import User as AiogramUser
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def add_user_to_db(user: AiogramUser, db_session) -> User:
    new_user = User(
        id=user.id,
        fullname=user.full_name,
        username=user.username,
    )
    db_session.add(new_user)
    await db_session.flush()
    return new_user


async def get_user_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> User | None:
    query = select(User).filter(User.id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar()
    return user
