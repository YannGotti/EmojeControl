import typing, json, os, asyncio

from aiogram import types

from loader import dp, bot
from messages import *

from aiogram.utils.exceptions import MessageNotModified

from keyboards.inline import *

from states import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

FILE_PATH = "user_data.json"
FILE_PATH_GAME = "data\\games_data.json"

async def addChatToJson(message: types.Message):
    game_info = {
        'chat_id': message.chat.id,
        'message_id' : -1,
        'invite_link': message.chat.invite_link,
        'game_active': False,
        'game': 
        [{
            'players': [],
            'rounds' : [],
            'stats': [],
            'round': -1,
            'action_user' : 0,
            'current_user' : 0,
            'current_fight' : 0,
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

async def setMessageIdGame(chat_id, message_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            chat['message_id'] = message_id

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def getMessageIdGame(chat_id):
    message_id = None
    round = -1

    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            message_id = chat['message_id']

    return message_id

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

async def setRound(chat_id, round):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                local_round = game["round"] = round

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def getRound(chat_id):
    data = None
    round = -1

    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for inf in chat["game"]:
                round = inf["round"]

    return round

async def addUsersJsonMash(mash, chat_id, new_round = None):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    round = -1
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for inf in chat["game"]:
                round = inf["round"]

    if (new_round):
        if (not new_round):
            return
    else:
        if (round != -1):
            return
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for inf in chat["game"]:
                inf["rounds"].append(mash)

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)

    await setRound(chat_id, 0)
    
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
                
                players["players"].append({'id': user.id, 'username': user.username or user.first_name, 'score': 0})
    
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
                    text += f"Игрок <b>{user['username']}</b> присоединился\n"
    
    return text 

async def getUsersForGame(chat_id):
    users = []
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for players in chat["game"]:
                for user in players["players"]:
                    users.append(user)
    
    return users 

async def getIdUsersForGame(chat_id):
    array = []
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for players in chat["game"]:
                for user in players["players"]:
                    array.append(user['id'])
    
    return array 

async def getActionUser(chat_id):
    action = 0
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                action = game["action_user"]
    
    return action 

async def setActionUser(chat_id, action):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                    game["action_user"] = action

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def setCurrentFight(chat_id, current_fight):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                    game["current_fight"] = current_fight

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def getCurrentFight(chat_id):
    current_fight = 0
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                current_fight = game["current_fight"]
    
    return current_fight 

async def getCountFightsInRound(chat_id):
    data = None
    count_fights = 0

    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for rounds in chat["game"]:
                count_fights = len(rounds["rounds"][await getRound(chat_id)]) - 1

    return count_fights 

async def joinGameCallback(callback_query: types.CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    await addUserForGame(callback_query.from_user, chat_id)

    text = f"Игра начинается, залетаааем.{await getStringUsersForGame(chat_id)}"

    await editMessage(message, text, keyJoinGame)
    await callback_query.answer()

async def createMashUsers(chat_id, users = None, new_round = False):
    if (not users):
        users = await getUsersForGame(chat_id)
    cells = int(len(users) / 2)
    first_player = None
    last_player = None

    mash = []
    

    for i in range(cells):
        if (cells == 1):
            first_player = users[0]
            last_player = users[1]
        else:
            first_player = users[i]
            last_player = users[i + 2]

        info = {
            '0' : first_player,
            '1' : last_player,
            'winner' : ''
        }
        mash.append(info)

    await addUsersJsonMash(mash, chat_id, new_round)

async def getCurrentActionUser(chat_id, action):
    user = None
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    round = await getRound(chat_id)
    current_fight = await getCurrentFight(chat_id)

    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                user = game["rounds"][round][current_fight][f'{action}']
    
    return user 

async def addStats(chat_id, stat):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                    game["stats"].append(stat)

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def getCountStatsUser(chat_id, user_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    count = 0
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                for stats in game["stats"]:
                    if(stats["id"] == user_id): count += 1
    
    return count

async def getMessagesIdUserStats(chat_id, user_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    messages = []
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                for stats in game["stats"]:
                    if(stats["id"] == user_id): messages.append(stats["message_id"])
    
    return messages

async def getScoreUserStats(chat_id, user_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)

    score = 0
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                for stats in game["stats"]:
                    if(stats["id"] == user_id): score += stats["score"]
    
    return score

async def setStateUsers(message: types.Message, chat_id, add_text = ""):
    actionUser = await getActionUser(chat_id)

    currentActionUser = await getCurrentActionUser(chat_id, actionUser)

    for user in await getIdUsersForGame(chat_id):
        state = dp.current_state(chat=chat_id, user=user)

        if (currentActionUser['id'] == user):
            await state.set_state(Game.StartGame)
        
        else:
            await state.set_state(Game.WaitGame)

    text = f"Раунд начался, прошу игрока <b>@{currentActionUser['username']}</b> бросить свои 3 мяча!"
    await editMessage(message, add_text + text)

async def setUserScoreInRound(chat_id, score):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
                for rounds in chat["game"]:
                    user = rounds["rounds"][await getRound(chat_id)][await getCurrentFight(chat_id)][f"{await getActionUser(chat_id)}"]
                    user["score"] = score
                        
                        

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)
    return

async def resetAfterRoundData(chat_id, fullReset = False):
    await setActionUser(chat_id, 0)
    await setCurrentFight(chat_id, 0)

    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    
    for chat in data:
        if(chat["chat_id"] == chat_id):
            for game in chat["game"]:
                    game["stats"] = []

    with open(FILE_PATH_GAME, "w") as file:
        json.dump(data, file, indent=4)


    if (fullReset):
        for chat in data:
            if(chat["chat_id"] == chat_id):
                for game in chat["game"]:
                        game["players"] = []
                        game["rounds"] = []
                        game["round"] = -1

        with open(FILE_PATH_GAME, "w") as file:
            json.dump(data, file, indent=4)

        for user in await getIdUsersForGame(chat_id):
            state = dp.current_state(chat=chat_id, user=user)
            await state.finish()

    return

async def getWinUsersLastRound(chat_id):
    data = None
    with open(FILE_PATH_GAME, "r") as file:
        data = json.load(file)
    win_users = []


    for chat in data:
        if(chat["chat_id"] == chat_id):
            for rounds in chat["game"]:
                for users in rounds["rounds"][await getRound(chat_id)]:
                    if (users["0"]["score"] > users["1"]["score"]):
                        users["winner"] = users["0"]["username"]
                        win_users.append(users["0"])
                    else:
                        users["winner"] = users["1"]["username"]
                        win_users.append(users["1"])

    return win_users
    
    


async def goGameCallback(callback_query: types.CallbackQuery): #функция запуска игры
    message = callback_query.message
    chat_id = message.chat.id

    if (await getCountUsersForGame(chat_id) < 4):
        text = f"Игра начинается, залетаааем.{await getStringUsersForGame(chat_id)}\n<b>Меньше 4 игроков нельзя!</b>\n"
        await editMessage(message, text, keyJoinGame)
        return
    
    await createMashUsers(chat_id)
    

    time = 5
    for i in range(5):
        await editMessage(message, f"Игра начнется через {time}!")
        await asyncio.sleep(1)
        time -= 1


    await setStateUsers(message, chat_id)

    await callback_query.answer()

async def closeGame(msg: types.Message, chat_id, win_users):
    await editMessage(msg, f"<b>Игра завершена!!\nПобедитель {win_users[0]['username']}!!</b>")

    await setRound(chat_id, 0)
    await resetAfterRoundData(chat_id, True)
    return

async def finishRound(msg: types.Message, chat_id):
    win_users = await getWinUsersLastRound(chat_id)

    if (len(win_users) == 1):
        await closeGame(msg, chat_id, win_users)
        return

    await createMashUsers(chat_id, win_users, True)

    round = await getRound(chat_id) + 1
    winners = ""

    for user in win_users:
        winners += f"\n<b>{user['username']} со счетом в {user['score']} очков</b>\n"

    await editMessage(msg, f"<b>{round} раунд закончен\n</b>"
                        f"Победители: " + winners)
    
    await asyncio.sleep(1)

    await setRound(chat_id, round)
    await resetAfterRoundData(chat_id)
    
    message = await bot.send_message(chat_id=chat_id, text='.', reply_to_message_id=msg.message_id)
    await setStateUsers(message, chat_id)

    return

async def setNextPlayerStep(message: types.Message, chat_id):
    for message_id in await getMessagesIdUserStats(chat_id, message.from_user.id):
        await asyncio.sleep(1.5)
        await bot.delete_message(chat_id, message_id)

    score = await getScoreUserStats(chat_id, message.from_user.id)

    await setUserScoreInRound(chat_id, score)

    if (await getActionUser(chat_id) == 1):

        await setCurrentFight(chat_id, await getCurrentFight(chat_id) + 1)
        await setActionUser(chat_id, 0)
    else:
        await setActionUser(chat_id, 1)

    text = f"Поздравляю игрока <b>{message.from_user.username or  message.from_user.first_name}</b> вы заработали {score} очков\n"
    msg = await bot.send_message(chat_id=chat_id, text='.', reply_to_message_id=await getMessageIdGame(chat_id))

    await setMessageIdGame(chat_id, msg.message_id)

    if (await getCurrentFight(chat_id) > await getCountFightsInRound(chat_id)):
        await finishRound(msg, chat_id)
        return
        

    await setStateUsers(msg, chat_id, text)



@dp.message_handler(state=Game.StartGame, content_types=types.ContentType.DICE)
async def my_state_handler(message: types.Message, state: FSMContext):

    chat_id = message.chat.id

    data = {
        'id': message.from_user.id,
        'username':  message.from_user.username or  message.from_user.first_name,
        'score' : message.dice.value,
        'message_id' : message.message_id
    }
    await addStats(chat_id, data)

    if (await getCountStatsUser(chat_id, message.from_user.id) == 3):

        await setNextPlayerStep(message, chat_id)

        await state.finish()
        return

    await state.set_state(Game.StartGame)

@dp.message_handler(state=Game.WaitGame, content_types=types.ContentTypes.all())
async def my_state_handler(message: types.Message, state: FSMContext):
    await asyncio.sleep(0.2)
    await message.delete()
    await state.set_state(Game.WaitGame)


async def editMessage(message: types.Message, text, keyboard = None):
    if (keyboard):
        await message.edit_text(text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        return
    await message.edit_text(text, parse_mode=types.ParseMode.HTML)

    
@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True