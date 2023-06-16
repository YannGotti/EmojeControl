import asyncio, json
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

FILE_DATA = "processes\\crypto_data.json"


async def selectCryptoRateList():
    data = None
    with open(FILE_DATA, "r") as file:
        data = json.load(file)

    for crypto in data:
        growth_percentage = crypto["growth_percentage"]
        if(len(growth_percentage) >= 2):
            crypto["rating"] = 0
            for value in growth_percentage[:2]:
                if(value > 0): crypto["rating"] += value

            crypto["growth_percentage"] = []


    with open(FILE_DATA, 'w') as file:
        json.dump(data, file, indent=4)


async def selectGrowthPercentage(last_value, new_value):
    growth_rate = ((new_value - last_value) / last_value) * 100
    return growth_rate

async def addCrypto(crypto_name, crypto_price):
    data_crypto = {
        'crypto_name' : crypto_name,
        'crypto_price' : crypto_price,
        'crypto_price_last' : crypto_price,
        'growth_percentage' : [],
        'rating' : 0
    }

    data = None
    with open(FILE_DATA, "r") as file:
        data = json.load(file)

    user_exists = any(crypto["crypto_name"] == crypto_name for crypto in data)
    if user_exists:
        for crypto in data:
            if (crypto["crypto_name"] == crypto_name):
                crypto["crypto_price"] = crypto_price

                growth_rate = await selectGrowthPercentage(crypto["crypto_price_last"], crypto["crypto_price"])

                if (growth_rate == 0.0): return

                crypto["crypto_price_last"] = crypto["crypto_price"]

                crypto["growth_percentage"].append(growth_rate)

        with open(FILE_DATA, 'w') as file:
            json.dump(data, file, indent=4)
        return

    data.append(data_crypto)

    with open(FILE_DATA, 'w') as file:
        json.dump(data, file, indent=4)

async def getCryptoCount():
    data = None
    with open(FILE_DATA, "r") as file:
        data = json.load(file)

    return len(data)


async def selectCrypto():
    crypto_data = cg.get_coins_markets(vs_currency='usd')

    for index, crypto in enumerate(crypto_data, start=1):
        await addCrypto(crypto["name"], crypto["current_price"])

async def main():
    while(True):
        await selectCrypto()
        await selectCryptoRateList()
        await asyncio.sleep(10)



# Запускаем цикл событий
asyncio.run(main())