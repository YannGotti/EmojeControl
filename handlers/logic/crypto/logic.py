import typing, json, os, asyncio

from aiogram import types

from loader import dp, bot
from messages import *

from keyboards.inline import *

from states import *

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

FILE_DATA_CRYPTO = "processes\\crypto_data.json"

async def selectLocalTopCrypto(count = 5):
    data = None
    with open(FILE_DATA_CRYPTO, "r") as file:
        data = json.load(file)

    sorted_data = sorted(data, key=lambda x: x["rating"], reverse=True)

    topValues = sorted_data[:count]

    return topValues


async def MonitoringTop(message: types.Message, state: FSMContext):
    while(await state.get_state() == Crypto.MonitoringTop.state):
        text = "<b>Топ 5 быстрорастущих криптовалют:</b>\n"
        crypts = await selectLocalTopCrypto()

        i = 0
        for crypto in crypts:
            i += 1
            text += f"{i}.{crypto['crypto_name']}. Цена {crypto['crypto_price']} USD\n"

        text += "<b>Данное сообщение будет автоматически обновляться при изменении данных пока вы не закончите мониторинг!</b>"
        await message.edit_text(text, reply_markup=cryptoStopMonitoring)
        await asyncio.sleep(60)

@dp.callback_query_handler(lambda c: c.data == 'topCrypto')
async def topCryptoHandler(callback_query: types.CallbackQuery, state: FSMContext):
    if not await state.get_state():
        await Crypto.MonitoringTop.set()
        await MonitoringTop(callback_query.message, state)

    await callback_query.answer()

@dp.callback_query_handler(state=Crypto.MonitoringTop)
async def stopMonitoringHandler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.edit_text("Мониторинг курсов криптовалют остановлен.")
    await asyncio.sleep(10)
    await callback_query.message.delete()
    await callback_query.answer()


@dp.message_handler(state=Crypto.MonitoringTop)
async def my_state_handler(message: types.Message, state: FSMContext):
    await asyncio.sleep(0.2)
    await message.delete()