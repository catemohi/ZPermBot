from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_cncl,kb_mm,kb_ds
from aiogram.dispatcher.filters import Text


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=kb_mm)
    await message.delete()

async def cmd_back(message: types.Message,state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Главное меню', reply_markup=kb_mm)
    await message.delete()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(cmd_back, Text(equals='Назад', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Сегодня', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Вчера', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Позавчера', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Завтра', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Послезавтра', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Другой день', ignore_case=True), state="*")
    dp.register_message_handler(cmd_back, Text(equals='Отмена', ignore_case=True), state="*")
