import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin = os.getenv("ADMIN_ID")
geoname = os.getenv('GEONAME')
pguser = os.getenv('POSTGRES_USER')
pgpassword = os.getenv('POSTGRES_PASSWORD')
pgdb = os.getenv('POSTGRES_DB')

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', retention='30 days', enqueue=True)
geo_string = 'http://' + 'api.geonames.org/timezoneJSON?lat={}&lng={}&username={}'
db_string = f"postgresql+psycopg2://{pguser}:{pgpassword}@0.0.0.0:5432/{pgdb}"
