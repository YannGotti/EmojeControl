import typing, json, os, asyncio

from aiogram import types

from loader import dp, bot
from messages import *

from aiogram.utils.exceptions import MessageNotModified

from keyboards.inline import *

FILE_PATH = "user_data.json"
FILE_PATH_GAME = "data\\games_data.json"




async def addChatToJson(message: types.Message):
    game_info = {
        'chat_id': message.chat.id,
        'invite_link': message.chat.invite_link,
        'game_active': False,
        'game': 
        [{
            'players': [],
            'rounds' : []
        }]
    }

    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    user_exists = any(int(chat["chat_id"]) == message.chat.id for chat in data)
    if user_exists:
        return

    data.append(game_info)

    with open(FILE_PATH_GAME, 'w') as file:
        json.dump(data, file, indent=4)

async def getActiveGame(message: types.Message, PATH_FILE = FILE_PATH_GAME):
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


async def addUserForGame(user: types.User, chat_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for players in chat["game"]:
                user_exists = any(int(users["id"]) == user.id for users in players['players'])
                if user_exists:
                    return
                
                players["players"].append({'id': user.id, 'username': user.username or user.first_name})
    
    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def getCountUsersForGame(chat_id):
    count = 0
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for players in chat["game"]:
                count = len(players["players"])
    
    return count 

async def getStringUsersForGame(chat_id):
    text = "\n"
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for players in chat["game"]:
                for user in players["players"]:
                    text += f"<b>Игрок {user['username']} присоединился</b>\n"
    
    return text 


async def joinGameCallback(callback_query: types.CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    await addUserForGame(callback_query.from_user, chat_id)

    text = f"Игра начинается, залетаааем.{await getStringUsersForGame(chat_id)}"

    await editMessage(message, text, keyJoinGame)
    await callback_query.answer()


async def goGameCallback(callback_query: types.CallbackQuery):
    message = callback_query.message

    if (await getCountUsersForGame(message.chat.id) < 2):
        text = f"Игра начинается, залетаааем.{await getStringUsersForGame(message.chat.id)}\n<b>Меньше 4 игроков нельзя!</b>\n"
        await editMessage(message, text, keyJoinGame)
        return

    time = 5
    for i in range(5):
        await editMessage(message, f"Игра начнется через {time}!")
        await asyncio.sleep(1)
        time -= 1



    await callback_query.answer()



async def editMessage(message: types.Message, text, keyboard = None):
    if (keyboard):
        await message.edit_text(text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        return
    await message.edit_text(text, parse_mode=types.ParseMode.HTML)

    
@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True