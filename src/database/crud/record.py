from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Record


async def get_record_by_id(record_id: int, db_session: AsyncSession) -> Record | None:
    query = select(Record).filter(Record.id == record_id)
    result = await db_session.execute(query)
    record = result.scalar()
    return record


async def create_record(record: Record, db_session: AsyncSession) -> None:
    db_session.add(record)
    await db_session.flush()


async def delete_record_from_user(record_id: int, db_session: AsyncSession) -> None:
    query = delete(Record).filter(Record.id == record_id)
    await db_session.execute(query)


async def get_all_records_from_user(
    user_id: int,
    db_session: AsyncSession,
) -> list[Record]:
    query = select(Record).where(
        Record.user_id == user_id,
    )
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def get_all_records(
    db_session: AsyncSession,
) -> list[Record]:
    query = select(Record)
    result = await db_session.execute(query)
    return list(result.scalars().all())
