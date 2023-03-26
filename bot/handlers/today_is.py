from aiogram import types
from bot.config import dp
from aiogram.dispatcher.filters import Command
from bot.utils.date import DateObj


today_is_text = (f'<b>Today is:</>\n'
                 f'\n'
                 f'{DateObj.dayofweek}, {DateObj.dayofmonth} {DateObj.month} (month progress: {DateObj.monthprogress}%)\n'
                 f'Day #{DateObj.dayofyear} of {DateObj.year} (year progress: {DateObj.yearprogress}%)\n'
                 f'Week #{DateObj.numberofweeks}\n')


@dp.message_handler(Command('today_is'))
async def today_is(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,
                              text=today_is_text)

