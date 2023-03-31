from aiogram.dispatcher.filters.builtin import Command
from bot.utils.keyboards import tools
from datetime import datetime
from loguru import logger
import dateutil.parser
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.utils.states import States
from bot.config import dp
from bot.replies import answer


@dp.message_handler(Command("tools"))
async def general_operations(message: types.Message):
    await message.answer(text=answer['tools_reply'], reply_markup=tools)


@dp.callback_query_handler(text=['days_counter', 'date_calculator'])
async def days_operations(call: types.CallbackQuery):
    if call.data == 'days_counter':
        await States.Counter.set()
        await call.message.answer(text=answer['days_counter_reply'])
        await call.answer()

    if call.data == 'date_calculator':
        await States.First_date.set()
        await call.message.answer(text=answer['date_calculator_reply'])
        await call.answer()


@dp.message_handler(state=States.Counter)
async def counter_input(message: types.Message, state: FSMContext):
    await States.Counter.set()
    date_for_count = message.text
    now = datetime.now()
    try:
        date1 = dateutil.parser.parse(date_for_count, dayfirst=True)
        period = now - date1
        if now.day == date1.day and now.month == date1.month and now.year == date1.year:
            await message.answer(f'Your date is today')
        elif now > date1:
            await message.answer(f'Your event was {period.days} days ago')
        else:
            period = date1 - now
            await message.answer(f'{int(period.days) + 1} days left until your event')
        await state.reset_state(with_data=False)
    except ValueError:
        await message.answer(f'Please, enter correct value. For example:\n'
                             f'\n'
                             f'<b>20 April 2000</> or <b>4.20.2000</>\n'
                             f'\n'
                             f'<b>/help</> for more info\n')
        logger.debug("Entered string '{}' is not good for date parsing", message.text)


@dp.message_handler(state=States.First_date)
async def calculator_input_first(message: types.Message, state: FSMContext):
    first_date = message.text
    try:
        date1 = dateutil.parser.parse(first_date, dayfirst=True)
        await state.update_data(input1=date1)
        await message.answer(f'Enter the second date:\n'
                             f'\n'
                             f'\n'
                             f'<i>read more about supported formats in /help section.</>\n')
        await States.Second_date.set()
    except ValueError:
        await message.answer(f'Please, enter correct value. For example:\n'
                             f'\n'
                             f'<b>20 April 2000</> or <b>4.20.2000</>\n'
                             f'\n'
                             f'<b>/help</> for more info\n')
        logger.debug("Entered string '{}' is not good for date parsing", message.text)


@dp.message_handler(state=States.Second_date)
async def calculator_input_second(message: types.Message, state: FSMContext):
    second_date = message.text
    try:
        date2 = dateutil.parser.parse(second_date, dayfirst=True)
        mydata = await state.get_data()
        date1 = mydata.get('input1')

        period = date2 - date1
        if date1.day == date2.day and date1.month == date2.month and date1.year == date2.year:
            await message.answer(f'Zero days between this dates')
        elif date2 > date1:
            await message.answer(f'{period.days} days between the dates')
        else:
            period = date1 - date2
            await message.answer(f'{period.days} days between the dates')
        await state.reset_state(with_data=False)
    except ValueError:
        await message.answer(f'Please, enter correct value. For example:\n'
                             f'\n'
                             f'<b>20 April 2000</> or <b>4.20.2000</>\n'
                             f'\n'
                             f'<b>/help</> for more info\n')
        logger.debug("Entered string '{}' is not good for date parsing", message.text)
