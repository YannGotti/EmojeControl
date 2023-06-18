import os, asyncio, json

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *
from config import ADMINS
from handlers.logic.basketball.logic import addChatToJson

from handlers.logic.basketball.logic import setActiveGame, joinGameCallback, addChatToJson, goGameCallback

FILE_PATH_GAME = "data\\games_data.json"

from keyboards.inline import cryptoKeyboard
from keyboards.MenuWebApp import webApp, webAppInlineButon

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    msg = await message.answer("Защита от спама, подождите 25 сек")
    await asyncio.sleep(5)
    await msg.delete()


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=5)
async def start_command_handler(message: types.Message):
    await addChatToJson(message)


@dp.message_handler(commands=['crypto'])
@dp.throttled(anti_flood, rate=5)
async def crypto_command_handler(message: types.Message):
    await message.answer('Менеджер криптовалют', reply_markup=cryptoKeyboard)

@dp.message_handler(commands=['game'])
@dp.throttled(anti_flood, rate=5)
async def crypto_command_handler(message: types.Message):
    if (message.chat.type == "supergroup"):
        await message.answer('Присоединиться к игре возможно только в личном сообщении!\n@mildor_bot')
        return
    
    await message.answer('Начать лучшую веб игру!', reply_markup=webAppInlineButon)

    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonWebApp(text="MildorGame", web_app=webApp),
    )


@dp.callback_query_handler(lambda c: True)
async def inline_button_handler(callback_query: types.CallbackQuery):

    if callback_query.data == "startGame" and callback_query.from_user.id in ADMINS:
        await setActiveGame(callback_query, FILE_PATH_GAME, True)
        await callback_query.answer("Вы запустили игру")

    elif callback_query.data == "stopGame" and callback_query.from_user.id in ADMINS:
        await setActiveGame(callback_query, FILE_PATH_GAME, False)
        await callback_query.answer("Вы закончили игру")

    elif callback_query.data == "joinGame":
        await joinGameCallback(callback_query)

    elif callback_query.data == "goGame" and callback_query.from_user.id in ADMINS:
        await goGameCallback(callback_query)