from aiogram import types

from config import WEBAPP_URL

webApp = types.WebAppInfo(url=WEBAPP_URL)

webAppInlineButon = types.InlineKeyboardMarkup()
webAppInlineButon.add(
    types.InlineKeyboardButton(text="Open Webview", web_app=webApp)
)

webAppKeyboard = types.MenuButtonWebApp(text="Начать игру", web_app=webApp)
