from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import dateutil.parser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.models import Record, User
from bot.config import dp, logger
from bot.replies import answer
from bot.utils.keyboards import add_record_keyboard, add_and_delete_keyboard
from bot.database import session
from sqlalchemy import literal
from bot.utils.states import States
from datetime import datetime, timedelta


def all_records_reply(user_id: int) -> str:
    all_records_query = session.query(Record).filter(Record.user_id == user_id)
    all_records = session.execute(all_records_query)
    user = session.query(User).filter(User.user_id == user_id).scalar()
    offset = user.utc_offset
    if not offset:
        now = datetime.utcnow()
    else:
        now = datetime.utcnow() + timedelta(hours=offset)

    event_number = 0
    all_records_reply = ''
    for row in all_records.fetchall():
        event = row[0]
        if now.day == event.event_date.day and now.month == event.event_date.month and now.year == event.event_date.year:
            ans = ' <b>today</>'
        elif now > event.event_date:
            period = now - event.event_date
            ans = (f' <b>{period.days}</> days ago')
        else:
            period = event.event_date - now
            ans = f' in <b>{period.days + 1}</> days'

        days_counter = now - event.event_date
        event_number += 1
        event_row = f"{event_number}. {event.event_name}{ans}\n"
        all_records_reply += event_row
    return all_records_reply


@dp.message_handler(Command('records'))
async def records_command(message: types.Message):
    db_record = session.query(Record.user_id).filter(Record.user_id == message.from_user.id)
    result = session.query(literal(True)).filter(db_record.exists()).scalar()
    if not result:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text=answer["records_reply_unregistered"], reply_markup=add_record_keyboard)
    else:
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text=all_records_reply(message.from_user.id), reply_markup=add_and_delete_keyboard)


@dp.callback_query_handler(text='add_record')
async def event_name(call: types.CallbackQuery):
    await dp.bot.send_message(chat_id=call.from_user.id,
                              text=answer["event_name_reply"])
    await States.Event_name.set()


@dp.message_handler(state=States.Event_name)
async def name_input(message: types.Message, state: FSMContext):
    event_name = message.text
    await state.update_data(event_name=event_name)
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=answer["event_date_reply"])
    await States.Event_date.set()


@dp.message_handler(state=States.Event_date)
async def date_input(message: types.Message, state: FSMContext):
    reply = message.text
    try:
        event_date = dateutil.parser.parse(reply, dayfirst=True)
        mydata = await state.get_data()
        event_name = mydata.get('event_name')
        record = Record(user_id=message.from_user.id,
                        event_name=event_name,
                        event_date=event_date,
                        created_at=datetime.utcnow())
        session.add(record)
        session.commit()
        session.close()
        await dp.bot.send_message(chat_id=message.from_user.id,
                                  text=all_records_reply(message.from_user.id), reply_markup=add_and_delete_keyboard)
        await state.reset_state(with_data=False)
    except ValueError as e:
        await message.answer(answer['value_error_reply'])
        logger.debug(answer['value_error_log'], message.from_user.id, e, message.text)


@dp.callback_query_handler(text='delete_record')
async def delete_record(call: types.CallbackQuery):
    query = session.query(Record).filter(Record.user_id == call.from_user.id)
    count = query.count()
    kb = ReplyKeyboardMarkup(row_width=4, one_time_keyboard=True, input_field_placeholder=answer["event_delete_placeholder"],
                             resize_keyboard=True)
    [kb.insert(KeyboardButton(text=f'{record}')) for record in range(1, count + 1)]
    [kb.insert(KeyboardButton(text='cancel', callback_data='cancel'))]
    await dp.bot.send_message(chat_id=call.from_user.id,
                              text=answer["event_delete_reply"],
                              reply_markup=kb)
    types.ReplyKeyboardRemove()
    await States.Delete_record.set()


@dp.message_handler(text='cancel', state=States.Delete_record)
async def delete_record(call: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await dp.bot.send_message(chat_id=call.from_user.id,
                              text=all_records_reply(call.from_user.id), reply_markup=add_and_delete_keyboard)


@dp.message_handler(state=States.Delete_record)
async def date_input(message: types.Message, state: FSMContext):
    record_number = int(message.text)
    db_record = session.query(Record.user_id).filter(Record.user_id == message.from_user.id)
    user_records = session.query(Record).filter(Record.user_id == message.from_user.id).all()
    selected_record = user_records[record_number - 1]
    session.delete(selected_record)
    session.commit()
    session.close()
    await state.reset_state(with_data=False)
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=all_records_reply(message.from_user.id), reply_markup=add_and_delete_keyboard)
