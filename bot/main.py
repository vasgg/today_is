from aiogram import executor
from handlers import dp
from middleware import AuthMiddleware

from bot.utils.notify_admin import on_shutdown_notify

if __name__ == '__main__':
    dp.middleware.setup(AuthMiddleware())
    executor.start_polling(dp, on_shutdown=on_shutdown_notify)
