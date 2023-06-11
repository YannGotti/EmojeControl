from aiogram import types

adminKey = types.InlineKeyboardMarkup(row_width=2)
adminKey.add(
    types.InlineKeyboardButton("Начать игру", callback_data="startGame"),
    types.InlineKeyboardButton("Закончить игру", callback_data="stopGame")
)


keyJoinGame = types.InlineKeyboardMarkup(row_width=1)
keyJoinGame.add(
    types.InlineKeyboardButton("Присоединиться", callback_data="joinGame", parse_mode=types.ParseMode.HTML),
    types.InlineKeyboardButton("Начать игру", callback_data="goGame", parse_mode=types.ParseMode.HTML)

)