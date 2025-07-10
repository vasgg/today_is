import logging
import os

from aiogram import Bot

from bot.config import Settings

logger = logging.getLogger(__name__)


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


async def on_startup(bot: Bot, settings: Settings) -> None:
    folder = get_folder_name()
    await notify_admin(
        bot,
        settings.bot.admin,
        f"<b>{folder} started</b>\n\n/start",
    )


async def on_shutdown(bot: Bot, settings: Settings) -> None:
    folder = get_folder_name()
    await notify_admin(
        bot,
        settings.bot.ADMINS[0],
        f"<b>{folder} shutdown</b>",
    )
