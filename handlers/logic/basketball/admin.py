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
from handlers.logic.basketball.logic import setActiveGame, joinGameCallback, addChatToJson, getActiveGame, goGameCallback, setMessageIdGame, resetAfterRoundData

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


@dp.message_handler(commands=['closegame'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def closegame(message: types.Message):
    await message.delete()
    if (not await getActiveGame(message)):
        mess = await message.answer("Вы не открыли игру!")
        await asyncio.sleep(3)
        await mess.delete()
        return
    
    await resetAfterRoundData(message.chat.id, True)

    mess = await message.answer("Игра была принудительно закончена!")
    await asyncio.sleep(3)
    await mess.delete()
    




