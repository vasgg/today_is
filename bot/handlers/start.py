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
    user_id = message.from_user.id
    now = datetime.utcnow()
    user = session.query(User).filter(User.user_id == user_id).scalar()

    # created_at = session.query(User.created_at).filter(User.user_id == user_id).scalar()
    # row = session.query(User).filter_by(id=User.user_id).first()
    # query = session.query(User.id, User.created_at)
    # for row in query:
    #     u = row._asdict()
    # cra = u['created_at']
    back = now - user.created_at
    print(user)
    reply = answer['start_reply'].format(message.from_user.full_name, user.id, user.created_at.strftime("%d %B %Y"), back.days)
    # print(id.created_at)
    await dp.bot.send_message(chat_id=user_id, text=reply)
