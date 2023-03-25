from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton



registration_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
registration_button.insert(KeyboardButton(text='Registration', request_location=True))

kb = InlineKeyboardMarkup(row_width=6)
[kb.insert(InlineKeyboardButton(text=f'{hour:02}', callback_data=hour)) for hour in range(24)]

kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=6)
kb2.insert(KeyboardButton(text=f'{hour:02}') for hour in range(24))
