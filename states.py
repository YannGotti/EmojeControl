from aiogram.dispatcher.filters.state import State, StatesGroup

class Game(StatesGroup):
    StartGame = State()
    WaitGame = State()

class Crypto(StatesGroup):
    MonitoringTop = State()
    MonitoringAll = State()