from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.utils.keyboards import records_button

from bot.config import dp
from bot.utils.times import DateObjects


@dp.message_handler(Command('today_is'))
async def today_is_command(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=DateObjects.today_is_reply)
