from datetime import datetime

import httpx
from aiogram import types
from sqlalchemy import update

from bot.config import geo_string, geoname, dp
from bot.database import session
from bot.models import User
from bot.replies import answer


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    geoname_string = geo_string.format(latitude, longitude, geoname)
    response = httpx.get(geoname_string).json()
    countryCode = response['countryCode'];
    utcOffset = response['gmtOffset'];
    timezoneId = response['timezoneId'];
    countryName = response['countryName'];
    sunrise = response['sunrise'];
    sunset = response['sunset'];
    reply = answer['location_reply'].format \
        (latitude, longitude, sunrise, sunset, countryName, countryCode, timezoneId, utcOffset)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())

    statement = update(User).where(User.user_id == message.from_user.id).values(utc_offset=utcOffset, updated_at=datetime.utcnow())
    session.execute(statement)
    session.commit()
    session.close()
