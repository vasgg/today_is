import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin = int(os.getenv("ADMIN_ID"))
geoname = os.getenv('GEONAME')
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

logger.add('../debug.log', format='{time} {level} {message}', level='DEBUG', retention='30 days', enqueue=True)
geo_string = 'http://'+'api.geonames.org/timezoneJSON?lat={}&lng={}&username={}'
db_string = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@0.0.0.0:5432/{os.getenv('POSTGRES_DB')}"

