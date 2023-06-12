import os, asyncio
import typing
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from loader import dp, bot
from messages import *
from config import ADMINS

from keyboards.inline import *
from handlers.logic.logic import setActiveGame, joinGameCallback, addChatToJson, getActiveGame, goGameCallback, setMessageIdGame

FILE_PATH_GAME = "data\\games_data.json"


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)

@dp.message_handler(commands=['admin'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def admin_panel(message: types.Message):
    await message.delete()
    await addChatToJson(message)
    await message.answer("Админ панель", reply_markup=adminKey)

@dp.message_handler(commands=['startgame'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def startgame(message: types.Message):
    await message.delete()
    if (not await getActiveGame(message)):
        mess = await message.answer("Вы не открыли игру!")
        await asyncio.sleep(3)
        await mess.delete()
        return

    mes = await message.answer("Игра начинается, залетаааем.", reply_markup=keyJoinGame)
    await setMessageIdGame(message.chat.id, mes.message_id)



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


@dp.message_handler(commands=['ale'], user_id=ADMINS)
async def admin_panel(message: types.Message):
    await message.delete()
    messages = []
    for i in range(5):
        messages.append(await message.answer("Я РУССКИЙ але)))"))

    for mesg in messages:
        await asyncio.sleep(0.3)
        await mesg.delete()