from datetime import datetime, timedelta, UTC
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from httpx import Client
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Settings
from bot.internal.controllers import get_location_reply_with_offset, compose_today_is_message
from bot.internal.keyboards import provide_location_kb
from bot.internal.replies import answer
from database.crud.record import get_all_records
from database.crud.user import get_users_count
from database.models import User

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_message(message: Message, user: User) -> None:
    offset = user.utc_offset
    if not offset:
        now = datetime.now(UTC)
    else:
        now = datetime.now(UTC) + timedelta(hours=offset)
    back = now - user.created_at
    reply = answer["start_reply"].format(user.firstname, user.created_at.strftime("%d %B %Y"), back.days)
    await message.answer(text=reply)


@router.message(Command("info"))
async def info_command(message: Message):
    await message.answer(
        text=answer["info_reply"],
    )


@router.message(Command("settings"))
async def settings_command(message: Message):
    await message.answer(text=answer["settings_reply"], reply_markup=provide_location_kb())


@router.message(Command("today_is"))
async def today_is_command(message: Message, user: User):
    offset = user.utc_offset
    if not offset:
        today = datetime.now(UTC)
    else:
        today = datetime.now(UTC) + timedelta(hours=offset)
    today_is_reply = compose_today_is_message(today)
    await message.answer(text=today_is_reply)


@router.message(F.location)
async def handle_location(message: Message, settings: Settings, user: User, db_session: AsyncSession):
    reply, utc_offset = await get_location_reply_with_offset(message, settings)
    await message.answer(reply, reply_markup=ReplyKeyboardRemove())
    user.utc_offset = utc_offset
    db_session.add(user)


@router.message(Command("statistics"))
async def statistics_is_command(message: Message, db_session: AsyncSession):
    user_count = await get_users_count(db_session)
    user_records = await get_all_records(db_session)
    reply = answer["statistics_reply"].format(user_count, len(user_records))
    await message.answer(text=reply)
