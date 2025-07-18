from aiogram import Bot, types

default_commands = [
    types.BotCommand(command="/start", description="first thing first"),
    types.BotCommand(command="/today_is", description="main command"),
    types.BotCommand(command="/records", description="all about your events"),
    types.BotCommand(command="/settings", description="location and timezone stuff"),
    types.BotCommand(command="/info", description="more info"),
]


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(default_commands)
