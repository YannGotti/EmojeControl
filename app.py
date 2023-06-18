from aiogram import Bot, types

from aiogram.types import BotCommand

from loader import bot, storage


async def set_default_commands(dp_local):
    await dp_local.bot.set_my_commands([
        BotCommand("startgame", "Играть"),
        #BotCommand("shop", "Магазин"),
        #BotCommand("profile", "Вызвать меню профиля"),
        #BotCommand("change_twitch", "Поменять никнейм Twitch")
    ])
    
    


async def on_shutdown():
    await storage.close()
    await bot.close()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True, on_startup=set_default_commands)

