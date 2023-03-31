from aiogram import types
from aiogram.dispatcher.filters import Command
from bot.models import Record
from bot.config import dp
from bot.replies import answer
from bot.utils.keyboards import add_record_button
from bot.database import session
from sqlalchemy import literal


@dp.message_handler(Command('records'))
async def records_command(message: types.Message):
    user_id = message.from_user.id
    db_record = session.query(Record.user_id).filter(Record.user_id == user_id)
    result = session.query(literal(True)).filter(db_record.exists()).scalar()
    if not result:
        await dp.bot.send_message(chat_id=user_id,
                                  text=answer["records_reply_unregistered"], reply_markup=add_record_button)


@dp.callback_query_handler(text='add_record')
async def vote_up_cb_handler(query: types.CallbackQuery):
    user_id = query.from_user.id
    await query.answer(cache_time=60)
    await dp.bot.send_message(chat_id=user_id,
                              text='testing stuff')
