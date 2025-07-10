import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from bot.config import Settings, get_settings
from bot.handlers.base import router as base_router
from bot.handlers.errors import router as errors_router
from bot.internal.commands import set_bot_commands
from bot.internal.helpers import setup_logs
from bot.internal.notify_admin import on_shutdown, on_startup
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.session import DBSessionMiddleware
from bot.middlewares.updates_dumper import UpdatesDumperMiddleware
from database.db_connector import get_db


async def main():
    setup_logs("bot")
    settings: Settings = get_settings()

    bot = Bot(token=settings.bot.token.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis_client = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        username=settings.redis.username,
        password=settings.redis.password.get_secret_value(),
        decode_responses=True,
    )
    storage = RedisStorage(redis_client)
    dispatcher = Dispatcher(storage=storage, settings=settings)
    db = get_db(settings)

    db_session_middleware = DBSessionMiddleware(db)
    dispatcher.message.middleware(db_session_middleware)
    dispatcher.callback_query.middleware(db_session_middleware)
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.startup.register(set_bot_commands)
    dispatcher.include_routers(base_router, errors_router)

    logging.info("bot started")
    await dispatcher.start_polling(bot)


def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
