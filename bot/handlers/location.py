from bot.config import dp, GEONAME
from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter

import httpx


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
