from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram import types
from bot.utils.keyboards import provide_location_button
from bot.config import dp
from bot.replies import answer


@dp.message_handler(CommandHelp())
async def settings_command(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=answer['help_reply'])
