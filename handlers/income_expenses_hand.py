from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.chat import ChatActions
from create_bot import bot
from sheets import s
from keyboards import kb_ie,kb_mm
from message_formatters import summary_information_fmt,money_movement_fmt,summary_information_and_money_movement_fmt
import aiogram.utils.markdown as fmt


async def income_expenses_start(message: types.Message):
    await message.delete()
    await message.answer('Выберете необходимое:',reply_markup=kb_ie)


async def summary_information(message: types.Message):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    income_expenses = summary_information_fmt(s.get_income_expenses())
    await message.answer(income_expenses,reply_markup=kb_mm,parse_mode="HTML")


async def money_movement(message: types.Message):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    income_expenses = money_movement_fmt(s.get_income_expenses())
    await message.answer(income_expenses,reply_markup=kb_mm,parse_mode="HTML")


async def summary_information_and_money_movement(message: types.Message):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    income_expenses = summary_information_and_money_movement_fmt(s.get_income_expenses())
    await message.answer(income_expenses,reply_markup=kb_mm,parse_mode="HTML")


def register_handlers_income_expenses(dp: Dispatcher):
    dp.register_message_handler(income_expenses_start, Text(equals='Доходы/Расходы', ignore_case=True))
    dp.register_message_handler(summary_information, Text(equals='Сводная информация', ignore_case=True))
    dp.register_message_handler(money_movement, Text(equals='Движения средств', ignore_case=True))
    dp.register_message_handler(summary_information_and_money_movement, Text(equals='Сводная информация и двежения средств', ignore_case=True))


    
