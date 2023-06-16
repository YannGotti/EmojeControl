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

cryptoKeyboard = types.InlineKeyboardMarkup(row_width=1)
cryptoKeyboard.add(
    types.InlineKeyboardButton("Топ 5 быстрорастущих криптовалют", callback_data="topCrypto", parse_mode=types.ParseMode.HTML),
    types.InlineKeyboardButton("Криптовалюты в реальном времени", callback_data="cryptoOnline", parse_mode=types.ParseMode.HTML)

)

cryptoStopMonitoring  = types.InlineKeyboardMarkup(row_width=1)
cryptoStopMonitoring.add(
    types.InlineKeyboardButton("Остановить мониторинг", callback_data="stopMonitoring", parse_mode=types.ParseMode.HTML),
)