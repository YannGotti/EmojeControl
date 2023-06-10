import os, asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *
from config import ADMINS

import json

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    msg = await message.answer("Защита от спама, подождите 25 сек")
    await asyncio.sleep(2)
    await msg.delete()


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=25)
async def start(message: types.Message):
    if (message.chat.type == "private"):
        return

@dp.message_handler(content_types=types.ContentType.DICE)
async def handle_dice(message: types.Message):
    if (message.chat.type == "private"):
        return
    
    if message.dice.emoji == '🏀' or message.dice.emoji == '🎲' or message.dice.emoji == '🎯' or message.dice.emoji == '⚽' or message.dice.emoji == '🎰' or message.dice.emoji == '🎳': 
        if message.from_user.id in ADMINS: 
            await message.answer('You are my master!')
            await message.answer(f'МАЭСТРО БРАВО!! {message.dice.value} очка!!')
            print(await message.from_user.get_user_profile_photos())
            return 
        
        msg = await bot.send_message(message.chat.id, f'You are not my master! Пососи @{message.from_user.username} !!!')

        await message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return
    
@dp.message_handler()
async def handle_dice(message: types.Message):
    photos = await message.from_user.get_profile_photos()
    latest_photo = photos.photos[0][0]

    msg = await message.answer_photo(latest_photo.file_id)
    await asyncio.sleep(5)
    await msg.delete()