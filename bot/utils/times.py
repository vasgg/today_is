from calendar import monthrange, isleap
from datetime import datetime, timedelta
from bot.database import session
from isoweek import Week
from aiogram import types
from bot.replies import answer
from bot.models import User


class DateObjects:
    today = datetime.now()
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
                                                     number_of_weeks, month_progress,
                                                     current_year, year_progress)
