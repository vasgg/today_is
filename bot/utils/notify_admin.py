from aiogram import Dispatcher
from bot.config import admin
from bot.middleware import AuthMiddleware


async def on_shutdown_notify(dp: Dispatcher):
    await dp.bot.send_message(admin, 'Bot shutdown')


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(admin, 'Bot started')
