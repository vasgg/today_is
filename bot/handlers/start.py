from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.config import dp
from bot.utils.keyboards import provide_location_button
from bot.models import User
from bot.database import session
from sqlalchemy import select, literal
from bot.utils.times import DateObjects
from bot.replies import answer


@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    user = session.query(User).filter(User.user_id == message.from_user.id).scalar()
    offset = user.utc_offset
    if not offset:
        now = datetime.utcnow()
    else:
        now = datetime.utcnow() + timedelta(hours=offset)
    back = now - user.created_at
    reply = answer['start_reply'].format(message.from_user.full_name, user.id, user.created_at.strftime("%d %B %Y"), back.days)
    await dp.bot.send_message(chat_id=message.from_user.id, text=reply)
