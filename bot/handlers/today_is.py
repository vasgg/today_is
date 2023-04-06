from calendar import monthrange, isleap
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Command
from isoweek import Week

from bot.config import dp
from bot.database import session
from bot.models import User
from bot.replies import answer


@dp.message_handler(Command('today_is'))
async def today_is_command(message: types.Message):
    user = session.query(User).filter(User.user_id == message.from_user.id).scalar()
    offset = user.utc_offset
    if not offset:
        today = datetime.utcnow()
    else:
        today = datetime.utcnow() + timedelta(hours=offset)

    current_year = datetime.now().year
    current_month = datetime.now().month
    days_of_year = 366 if isleap(current_year) else 365
    month_name = today.strftime('%B')
    day_of_week = today.strftime('%A')
    day_of_month = today.strftime('%d')
    day_of_year = today.strftime('%j')
    year_progress = round(int(day_of_year) / days_of_year * 100)
    month_progress = round(int(day_of_month) / monthrange(current_year, current_month)[1] * 100)
    number_of_week = Week.thisweek().week
    number_of_weeks = str(Week.last_week_of_year(current_year))[-2:]
    today_is_reply = answer['today_is_reply'].format(day_of_week, month_name, day_of_month, day_of_year, days_of_year, number_of_week,
                                                     number_of_weeks, month_progress, current_year, year_progress)

    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=today_is_reply)
