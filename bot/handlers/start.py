from datetime import datetime
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from bot.config import dp
from bot.utils.keyboards import registration_button
from bot.models import User
from bot.database import session
from sqlalchemy import select, literal

@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    user_id = message.from_user.id
    now = datetime.utcnow()
    db_user = session.query(User.user_id).filter(User.user_id == user_id)
    id = session.query(User.id).filter(User.user_id == user_id).first()[0]
    registred_since = session.query(User.created_at).filter(User.user_id == user_id).first()[0]
    back = now - registred_since


    result = session.query(literal(True)).filter(db_user.exists()).scalar()

    if not result:

        await dp.bot.send_message(chat_id=user_id,
                                  text=f'Greetings, {message.from_user.full_name}.\n'
                                       f"Let's begin with <b>/today_is</> command\n"
                                       f'\n'
                                       f'For acess to base features go to <b>/tools</>\n'
                                       f'\n'
                                       f'If you wanna collect records about your events\n'
                                       f'please push the registration button bellow:\n')
        user = User(user_id=message.from_user.id,
                    firstname=message.from_user.first_name,
                    lastname=message.from_user.last_name,
                    username=message.from_user.username,
                    created_at=now,
                    updated_at=now,
                    language_code=message.from_user.language_code)
        session.add(user)
        session.commit()
        session.close()
    else:
        await dp.bot.send_message(chat_id=user_id,
                                  text=f'Greetings, {message.from_user.full_name}. '
                                       f'You are listed in the database since {registred_since}\n'
                                       f'days ago: <b>{back.days}</>\n'
                                       f'Registration record <b>#{id}</>\n', reply_markup=registration_button)
