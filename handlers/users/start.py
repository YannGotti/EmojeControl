import os, asyncio, json

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *
from config import ADMINS
from handlers.logic.basketball.logic import addChatToJson


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    msg = await message.answer("Защита от спама, подождите 25 сек")
    await asyncio.sleep(2)
    await msg.delete()


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=5)
async def start_command_handler(message: types.Message):
    await addChatToJson(message)
