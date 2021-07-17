# -*- coding: utf8 -*-
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import dialogs

print('Hello. Let\'s start.')
print('This robot fetches CleanTalk API.')


# Setup bot commands
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


# Main module
async def main():
    print('Main module started')

    # Init bot and dispatcher
    bot = Bot(token="1412332176:AAHq49t5iI3p5Mc4jyH375CE5EbGRwFHLwE", parse_mode="HTML")
    dp = Dispatcher(bot, storage=MemoryStorage())

    # handlers registration from dialogs.py
    dialogs.register_handlers(dp)

    # Run commands setup
    await set_commands(bot)

    # AIO polling startup
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

# Run project
if __name__ == '__main__':
    asyncio.run(main())
