import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
admin = int(os.getenv("ADMIN_ID"))
GEONAME = os.getenv('GEONAME')
logger.add('../debug.log', format='{time} {level} {message}', level='DEBUG', retention='30 days', enqueue=True)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

db_string = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@0.0.0.0:5432/{os.getenv('POSTGRES_DB')}"

