import os
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
from handlers.logic.logic import setActiveGame, joinGameCallback

FILE_PATH_GAME = "data\\games_data.json"


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)

@dp.message_handler(commands=['admin'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def admin_panel(message: types.Message):
    await message.delete()
    await message.answer("Админ панель", reply_markup=adminKey)

@dp.message_handler(commands=['startgame'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def startgame(message: types.Message):
    await message.delete()
    await message.answer("Игра начинается, залетаааем.", reply_markup=joinGame)


@dp.callback_query_handler(lambda c: True)
async def inline_button_handler(callback_query: types.CallbackQuery):

    if callback_query.from_user.id not in ADMINS:
        await callback_query.answer("У вас нет прав!")
        return

    if callback_query.data == "startGame":
        await setActiveGame(callback_query, FILE_PATH_GAME, True)
        await callback_query.answer("Вы запустили игру")

    elif callback_query.data == "stopGame":
        await setActiveGame(callback_query, FILE_PATH_GAME, False)
        await callback_query.answer("Вы закончили игру")

    elif callback_query.data == "joinGame":
        await joinGameCallback(callback_query)

