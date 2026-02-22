from calendar import isleap, monthrange
from datetime import UTC, datetime, timedelta, timezone
import logging

from dateutil.relativedelta import relativedelta

from aiogram.types import Message
from httpx import Client
from isoweek import Week

from bot.config import Settings
from bot.internal.replies import answer
from database.models import Record, User

logger = logging.getLogger(__name__)


def get_period_detail(earlier: datetime, later: datetime) -> str:
    rd = relativedelta(later, earlier)
    if rd.years == 0 and rd.months == 0:
        return ""
    parts = []
    if rd.years > 0:
        parts.append(f"<b>{rd.years}</b>y")
    if rd.months > 0:
        parts.append(f"<b>{rd.months}</b>m")
    if rd.days > 0:
        parts.append(f"<b>{rd.days}</b>d")
    if len(parts) >= 2:
        return ", ".join(parts[:-1]) + " and " + parts[-1]
    return parts[0]


def get_event_date(user_offset: int | None, event_date: datetime) -> str:
    if event_date.tzinfo is None:
        return event_date.strftime("%d.%m.%Y")
    if user_offset is None:
        return event_date.astimezone(UTC).strftime("%d.%m.%Y")
    user_timezone = timezone(timedelta(hours=user_offset))
    return event_date.astimezone(user_timezone).strftime("%d.%m.%Y")


def format_event_date_markup(user_offset: int | None, event_date: datetime) -> str:
    date_parts = get_event_date(user_offset, event_date).split(".")
    return ".".join(f"{part}" for part in date_parts)


def get_date_suffix(user_offset: int | None, record: Record) -> str:
    if not user_offset:
        now = datetime.now(UTC)
    else:
        now = datetime.now(UTC) + timedelta(hours=user_offset)
    if (
        now.day == record.event_date.day
        and now.month == record.event_date.month
        and now.year == record.event_date.year
    ):
        suffix = "<b>today</b>"
    elif now > record.event_date:
        period = now - record.event_date
        day_word = "day" if period.days == 1 else "days"
        suffix = f"<b>{period.days}</b> {day_word} ago"
        detail = get_period_detail(record.event_date, now)
        if detail:
            suffix += f" ({detail})"
    else:
        period = record.event_date - now
        days_left = period.days + 1
        day_word = "day" if days_left == 1 else "days"
        suffix = f"in <b>{days_left}</b> {day_word}"
        detail = get_period_detail(now, record.event_date)
        if detail:
            suffix += f" ({detail})"
    return suffix


def compose_all_records_reply(user_offset: int | None, records: list[Record]) -> str:
    all_records_reply = ""
    for i, record in enumerate(records, start=1):
        event_date = format_event_date_markup(user_offset, record.event_date)
        suffix = get_date_suffix(user_offset, record)
        event_row = f"{i}. <b>{record.event_name}</b> — {event_date}\n    {suffix}\n"
        all_records_reply += event_row
    return all_records_reply


def compose_today_is_message(today: datetime) -> str:
    current_year = today.year
    current_month = today.month
    days_of_year = 366 if isleap(current_year) else 365
    month_name = today.strftime("%B")
    day_of_week = today.strftime("%A")
    day_of_month = today.strftime("%d")
    day_of_year = today.strftime("%j")
    year_progress = round(int(day_of_year) / days_of_year * 100)
    month_progress = round(int(day_of_month) / monthrange(current_year, current_month)[1] * 100)
    number_of_week = Week.withdate(today.date()).week
    number_of_weeks = str(Week.last_week_of_year(current_year))[-2:]
    today_is_reply = answer["today_is_reply"].format(
        day_of_week,
        month_name,
        day_of_month,
        day_of_year,
        days_of_year,
        number_of_week,
        number_of_weeks,
        month_name,
        month_progress,
        current_year,
        year_progress,
    )
    return today_is_reply


async def get_location_reply_with_offset(message: Message, settings: Settings):
    latitude = message.location.latitude
    longitude = message.location.longitude
    geoname_string = settings.bot.geostring.get_secret_value().format(latitude, longitude, settings.bot.geoname)
    with Client() as client:
        try:
            response = client.get(geoname_string)
            response.raise_for_status()
            data = response.json()
            country_code = data.get("countryCode")
            utc_offset = data.get("gmtOffset")
            timezone_id = data.get("timezoneId")
            country_name = data.get("countryName")
            sunrise = data.get("sunrise")
            sunset = data.get("sunset")
        except Exception as e:
            logger.error(f"Failed to get location: {e}")
            return answer["geodata_error"]
    reply = answer["location_reply"].format(
        latitude, longitude, sunrise, sunset, country_name, country_code, timezone_id, utc_offset
    )
    return reply, utc_offset
