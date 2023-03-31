from aiogram import Dispatcher
from config import admin
from bot.middleware import AuthMiddleware


async def on_shutdown_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(admin, 'Bot shutdown')
    except Exception as err:
        logger.debug("'{}' is fatal error", err)
