from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

provide_location_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
provide_location_button.insert(KeyboardButton(text='update location', request_location=True))

records_button = InlineKeyboardMarkup()
records_button.insert(InlineKeyboardButton(text='records', callback_data='records'))

add_record_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='add record', callback_data='add_record')],
                                                          [InlineKeyboardButton(text='cancel', callback_data='cancel')]], row_width=2)

buttons = [[InlineKeyboardButton(text='🕛 days counter', callback_data='days_counter'),
            InlineKeyboardButton(text='🗓️ date calculator', callback_data='date_calculator')]]
tools = InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)
