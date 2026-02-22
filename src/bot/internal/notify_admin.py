from asyncio import CancelledError, Task, create_task, sleep
from contextlib import suppress
from datetime import datetime, timedelta
import logging
import os
from zoneinfo import ZoneInfo

from aiogram import Bot

from bot.config import Settings
from bot.internal.controllers import compose_today_is_message

logger = logging.getLogger(__name__)
TBILISI_TZ = ZoneInfo("Asia/Tbilisi")
MONDAY = 0
NOTIFY_HOUR = 13
NOTIFY_MINUTE = 0
weekly_today_is_task: Task[None] | None = None


def get_folder_name() -> str:
    return os.path.basename(os.getcwd()).replace("_", " ")


async def notify_admin(bot: Bot, admin_id: int, text: str) -> None:
    try:
        await bot.send_message(
            admin_id,
            text,
            disable_notification=True,
        )
    except Exception as exc:
        logger.warning("Failed to send admin notification: %r", exc, exc_info=True)


def get_seconds_until_next_monday_13(now: datetime) -> float:
    target = now.replace(hour=NOTIFY_HOUR, minute=NOTIFY_MINUTE, second=0, microsecond=0)
    days_until_monday = (MONDAY - now.weekday()) % 7
    target += timedelta(days=days_until_monday)
    if target <= now:
        target += timedelta(days=7)
    return (target - now).total_seconds()


async def weekly_today_is_notify_loop(bot: Bot, admin_id: int) -> None:
    while True:
        now = datetime.now(TBILISI_TZ)
        wait_seconds = get_seconds_until_next_monday_13(now)
        next_run = now + timedelta(seconds=wait_seconds)
        logger.info("Weekly admin today_is scheduled for %s", next_run.isoformat())
        await sleep(wait_seconds)
        today_is_reply = compose_today_is_message(datetime.now(TBILISI_TZ))
        await notify_admin(bot, admin_id, today_is_reply)


async def on_startup(bot: Bot, settings: Settings) -> None:
    global weekly_today_is_task
    folder = get_folder_name()
    await notify_admin(
        bot,
        settings.bot.admin,
        f"<b>{folder} started</b>\n\n/start",
    )
    if weekly_today_is_task is None or weekly_today_is_task.done():
        weekly_today_is_task = create_task(weekly_today_is_notify_loop(bot, settings.bot.admin))


async def on_shutdown(bot: Bot, settings: Settings) -> None:
    global weekly_today_is_task
    if weekly_today_is_task is not None:
        weekly_today_is_task.cancel()
        with suppress(CancelledError):
            await weekly_today_is_task
        weekly_today_is_task = None
    folder = get_folder_name()
    await notify_admin(
        bot,
        settings.bot.admin,
        f"<b>{folder} shutdown</b>",
    )
