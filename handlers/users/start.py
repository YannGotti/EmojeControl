import os, asyncio

from aiogram import types
from aiogram.dispatcher.filters import CommandStart, Text

from loader import dp, bot
from messages import *
from config import ADMINS

game_active = False

scores = {}

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.delete()
    msg = await message.answer("Защита от спама, подождите 25 сек")
    await asyncio.sleep(2)
    await msg.delete()


@dp.message_handler(CommandStart())
@dp.throttled(anti_flood, rate=25)
async def start_command_handler(message: types.Message):
    global game_active

    if (not game_active):
        return
    
    scores.clear()
    await message.reply("Добро пожаловать в турнир по бросанию emoji баскетбольного мяча! "
                        "Чтобы бросить мяч, просто отправьте его в чат.")

@dp.message_handler(content_types=types.ContentType.DICE)
async def handle_dice(message: types.Message):
    if (message.chat.type == "private"):
        return
    
    global game_active

    if (not game_active):
        return
    
    if message.dice.emoji == "🏀":
        player_id = message.from_user.id
        player_name = message.from_user.username or message.from_user.first_name
        msg = None

        await asyncio.sleep(4)

        scores[player_name] = scores.get(player_name, 0) + message.dice.value
        msg = await message.reply(f"Отлично, {player_name}! Вы набрали {message.dice.value} {format_score(message.dice.value)}. У вас всего {scores[player_name]} {format_score(message.dice.value)}.")
        await asyncio.sleep(2)
        await msg.delete()
        await message.delete()
        
    
    #if message.dice.emoji == '🏀' or message.dice.emoji == '🎲' or message.dice.emoji == '🎯' or message.dice.emoji == '⚽' or message.dice.emoji == '🎰' or message.dice.emoji == '🎳': 
    #    if message.from_user.id in ADMINS: 
    #        await message.answer('You are my master!')
    #        await message.answer(f'МАЭСТРО БРАВО!! {message.dice.value} очка!!')
    #        return 
    #    
    #    msg = await bot.send_message(message.chat.id, f'You are not my master! Пососи @{message.from_user.username} !!!')
        #await message.delete()
        #await asyncio.sleep(5)
        #await msg.delete()
        #return


@dp.callback_query_handler(lambda c: True)
async def inline_button_handler(callback_query: types.CallbackQuery):

    global game_active

    if callback_query.from_user.id not in ADMINS:
        await callback_query.answer("У вас нет прав!")
        return

    if callback_query.data == "startGame":
        game_active = True
        await callback_query.answer("Вы запустили игру")

    elif callback_query.data == "stopGame":
        game_active = False
        await callback_query.answer("Вы закончили игру")
    



@dp.message_handler(commands=['results'], user_id=ADMINS)
async def results_command_handler(message: types.Message):
    

    if scores:
        winner = max(scores, key=scores.get)

        text = ""

        for name, score in scores.items():
            text += (f'Игрок {name} - {score} {format_score(score)} \n')

        await message.reply(f"Результаты турнира:\n\n"
                            f"{text}\n"
                            f"<b>Победитель {winner}!!</b>", parse_mode=types.ParseMode.HTML)
    else:
        await message.reply("Пока еще никто не набрал очков в турнире.")


def format_score(score):
    if (score == 1): return 'очко'
    if (score > 1 and score < 5): return 'очка'
    if (score > 4): return 'очков'

@dp.message_handler(commands=['hi'])
async def handle_dice(message: types.Message):
    photos = await message.from_user.get_profile_photos()
    latest_photo = photos.photos[0][0]

    msg = await message.answer_photo(latest_photo.file_id)
    await asyncio.sleep(1)
    await message.delete()
    await msg.delete()


