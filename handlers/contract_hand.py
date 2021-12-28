from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from sheets import s
from keyboards import kb_cncl,kb_mm,kb_ds
import aiogram.utils.markdown as fmt
from message_formatters import contract_fmt

class ContractDay(StatesGroup):
    waiting_selected_button = State()
    choosing_another_day = State()


async def contract_start(message: types.Message):
    await message.delete()
    await message.answer('Выберете день, проверки сроков:',reply_markup=kb_ds)
    await ContractDay.waiting_selected_button.set()


async def checking_deadlines_for_today(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    twenty_days_contract = contract_fmt(s.twenty_days_contract(),'20ый')
    forty_days_contract = contract_fmt(s.forty_days_contract(),'40ой')
    await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
    await message.answer(forty_days_contract,parse_mode="HTML")
    await state.finish()


async def checking_deadlines_for_yesterday(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    twenty_days_contract = contract_fmt(s.twenty_days_contract(-1),'20ый')
    forty_days_contract = contract_fmt(s.forty_days_contract(-1),'40ой')
    await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
    await message.answer(forty_days_contract,parse_mode="HTML")
    await state.finish()


async def checking_deadlines_for_day_before_yesterday(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    twenty_days_contract = contract_fmt(s.twenty_days_contract(-2),'20ый')
    forty_days_contract = contract_fmt(s.forty_days_contract(-2),'40ой')
    await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
    await message.answer(forty_days_contract,parse_mode="HTML")
    await state.finish()
    

async def checking_deadlines_for_tomorrow(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    twenty_days_contract = contract_fmt(s.twenty_days_contract(1),'20ый')
    forty_days_contract = contract_fmt(s.forty_days_contract(1),'40ой')
    await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
    await message.answer(forty_days_contract,parse_mode="HTML")
    await state.finish()


async def checking_deadlines_for_day_after_tomorrow(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
    twenty_days_contract = contract_fmt(s.twenty_days_contract(2),'20ый')
    forty_days_contract = contract_fmt(s.forty_days_contract(2),'40ой')
    await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
    await message.answer(forty_days_contract,parse_mode="HTML")
    await state.finish()


async def choosing_another_day(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(fmt.text(
            fmt.text('Укажите день числом смещения от сегодня.'),
            fmt.text(fmt.hitalic('Например: вчера это -1')),
            sep='\n'),reply_markup=kb_cncl,parse_mode="HTML")
    await ContractDay.choosing_another_day.set()


async def checking_deadlines_for_another_day(message: types.Message, state: FSMContext):
    await message.delete()
    try: 
        number = float(message.text)
        await bot.send_chat_action(message.from_user.id,ChatActions.TYPING)
        twenty_days_contract = contract_fmt(s.twenty_days_contract(number),'20ый')
        forty_days_contract = contract_fmt(s.forty_days_contract(number),'40ой')
        await message.answer(twenty_days_contract,reply_markup=kb_mm, parse_mode="HTML")
        await message.answer(forty_days_contract,parse_mode="HTML")
        await state.finish()
    except ValueError:
        await message.answer(fmt.text(
            fmt.text(fmt.hbold('Ошибка данных!')),
            fmt.text('Укажите день числом смещения от сегодня.'),
            fmt.text(fmt.hitalic('Например: вчера это -1')),
            sep='\n'
        ),reply_markup=kb_cncl,parse_mode="HTML")
        return
    
async def checking_deadlines_for_another_day_cancel(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Выберете день, проверки сроков:',reply_markup=kb_ds)
    await ContractDay.waiting_selected_button.set()

def register_handlers_contract(dp: Dispatcher):
    dp.register_message_handler(contract_start, Text(equals='Договоры', ignore_case=True), state=None )
    dp.register_message_handler(checking_deadlines_for_today, Text(equals='Сегодня', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(checking_deadlines_for_yesterday, Text(equals='Вчера', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(checking_deadlines_for_day_before_yesterday, Text(equals='Позавчера', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(checking_deadlines_for_tomorrow, Text(equals='Завтра', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(checking_deadlines_for_day_after_tomorrow, Text(equals='Послезавтра', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(choosing_another_day, Text(equals='Другой день', ignore_case=True), state=ContractDay.waiting_selected_button)
    dp.register_message_handler(checking_deadlines_for_another_day_cancel, Text(equals='Отмена', ignore_case=True), state=ContractDay.choosing_another_day)
    dp.register_message_handler(checking_deadlines_for_another_day, state=ContractDay.choosing_another_day)

    
