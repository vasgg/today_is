from bot.config import dp, GEONAME
from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from sqlalchemy import update
from bot.models import User
from bot.database import session

import httpx

now = datetime.utcnow()

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    geoname_string = "http://"+f"api.geonames.org/timezoneJSON?lat={latitude}&lng={longitude}&username={GEONAME}"
    response = httpx.get(geoname_string).json()
    countryCode = response['countryCode'];
    utcOffset = response['gmtOffset'];
    timezoneId = response['timezoneId'];
    countryName = response['countryName'];
    reply = "latitude:  {}\nlongitude: {}\ncountryCode:  {}\nutcOffset: {}\ntimezoneId:  {}\ncountryName: {}\n".format\
        (latitude, longitude, countryCode, utcOffset, timezoneId, countryName)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())


    stmt = update(User).where(User.user_id == message.from_user.id).values(utc_offset=utcOffset, updated_at=now)
    session.execute(stmt)
    session.commit()
    session.close()
