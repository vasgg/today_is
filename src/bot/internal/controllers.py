from datetime import UTC, datetime, timedelta
from database.models import Record


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
        suffix = " <b>today</b>"
    elif now > record.event_date:
        period = now - record.event_date
        suffix = f" <b>{period.days}</b> days ago"
    else:
        period = record.event_date - now
        suffix = f" in <b>{period.days + 1}</b> days"
    return suffix


def compose_all_records_reply(user_offset: int | None, records: list[Record]) -> str:
    all_records_reply = ""
    for i, record in enumerate(records, start=1):
        suffix = get_date_suffix(user_offset, record)
        event_row = f"<b>{i}</b>. {record.event_name}{suffix}\n"
        all_records_reply += event_row
    return all_records_reply
