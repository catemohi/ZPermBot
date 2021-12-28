from aiogram import Bot
from aiogram.dispatcher import Dispatcher, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from my_filtres import AdminFilter,NotUserFilter
from auth import token

#Модуль для избежания import loop.
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(NotUserFilter)

