from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.config import dp, redis
from bot.database import session
from bot.models import User, Record
from bot.replies import answer


@dp.message_handler(Command('statistics'))
async def statistics_is_command(message: types.Message):
    user_count = session.query(User).count()
    user_records = session.query(Record).count()
    common_counter = redis.get('total')
    user_counter = redis.get(f'user:{message.from_user.id}')

    reply = answer['statistics_reply'].format(user_count, user_records, common_counter, user_counter)
    await dp.bot.send_message(chat_id=message.from_user.id, text=reply)
