from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandSettings
from bot.utils.keyboards import provide_location_button
from bot.config import dp
from bot.replies import answer


@dp.message_handler(CommandSettings())
async def settings_command(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=answer["settings_reply"], reply_markup=provide_location_button)
