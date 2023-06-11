import typing, json, os, asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData

from loader import dp, bot
from messages import *

FILE_PATH = "user_data.json"


async def getActiveGame(message: types.Message, PATH_FILE):
    data = None
    game_active = False
    with open(PATH_FILE, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == message.chat.id):
            game_active = chat['game_active']
    return game_active

async def setActiveGame(callback_query: types.CallbackQuery, PATH_FILE, game_active):
    data = None
    with open(PATH_FILE, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == callback_query.message.chat.id):
            chat['game_active'] = game_active

    
    with open(PATH_FILE, "w") as file:
        json.dump(data, file, indent=4)
    return

def read_user_data():
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

def write_user_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

async def select_info_user(message: types.Message):
    # Получение информации о пользователе
    user_id = message.from_user.id
    user = message.from_user

    data = read_user_data()

    user_exists = any(user["id"] == user_id for user in data)

    if user_exists:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)

        for user in data:
            if(user["id"] == user_id):
                user["values_dice"].append({"data" : json.dumps(message.date, default=str),'chat_id': message.chat.id, 'value_dice': message.dice.value})

        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
        return

    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        "is_premium": user.is_premium,
        "can_join_groups": user.can_join_groups,
        "can_read_all_group_messages": user.can_read_all_group_messages,
        "supports_inline_queries": user.supports_inline_queries,
        "last_emoji": message.dice.emoji,
        "first_score": message.dice.value,
        "values_dice": []
    }

    # Чтение текущих данных из файла
    with open(FILE_PATH, "r") as file:
        data = json.load(file)

    # Добавление новых данных в список
    data.append(user_data)

    # Запись обновленных данных в файл
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

    return

async def joinGameCallback(callback_query: types.CallbackQuery):
    await callback_query.answer('хуй')
    
    message = callback_query.message.text
    print(message)