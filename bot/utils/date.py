from calendar import monthrange
from datetime import datetime


class DateObjects:
    today = datetime.now()
    current_year = datetime.now().year
    current_month = datetime.now().month
    dayofweek = today.strftime('%A')
    dayofmonth = today.strftime('%-d')
    dayofyear = today.strftime('%j')
    yearprogress = round(int(today.strftime('%j')) / 365 * 100)
    monthprogress = round(int(today.strftime('%d')) / monthrange(current_year, current_month)[1] * 100)
    month = today.strftime('%B')
    year = today.strftime('%Y')
    numberofweeks = today.strftime('%V')
