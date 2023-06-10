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

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    await message.edit_text(ANTI_FLOOD)

@dp.message_handler(commands=['admin'], user_id=ADMINS)
@dp.throttled(anti_flood, rate=0)
async def admin_panel(message: types.Message):
    await message.delete()
    await message.answer("Админ панель")

