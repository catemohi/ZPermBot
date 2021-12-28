from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from create_bot import bot
from sheets import s
from keyboards import kb_cncl,kb_a
import aiogram.utils.markdown as fmt



class AddUser(StatesGroup):
    input_name_for_add = State()
    input_id_for_add = State()

class RemoveUser(StatesGroup):
    input_id_for_remove = State()

class AdminRights(StatesGroup):
    input_id_for_add = State()
    input_id_for_remove = State()


async def admin_start(message: types.Message):
    await message.answer(fmt.text(
        fmt.text(fmt.hbold('Доброго времени суток!')),
        fmt.text(fmt.hitalic('Выберете команду.')),
        sep='\n'
    ),parse_mode="HTML",reply_markup=kb_a)
    await message.delete()

async def not_admin_answer(message: types.Message):
    await message.answer(fmt.text(
        fmt.text(fmt.hbold('Ошибка!')),
        fmt.text(fmt.hitalic('Вы не администратор.')),
        sep='\n'
    ),parse_mode="HTML")
    await message.delete()


async def add_user_start(message: types.Message):
    await message.answer("Введите имя пользователя:", reply_markup=kb_cncl)
    await AddUser.input_name_for_add.set()
    await message.delete()


async def add_name_user(message: types.Message, state: FSMContext):
    if not message.text.replace(' ','').isalpha():
        await message.answer("Имя может состоят только из букв.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        return
    await state.update_data(name_user=' '.join(message.text.split()).lower().title())
    await AddUser.next()
    await message.answer("Теперь введите телеграм ID пользователя:", reply_markup=kb_cncl)
    await message.delete()


async def add_telegram_id_user(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Телеграм ID состоят только из цифр.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        return
    await state.update_data(telegram_id=int(message.text))
    user_data = await state.get_data()
    try:
        s.add_user([user_data['name_user'],user_data['telegram_id']])
    except:
        s.add_user([user_data['name_user'],user_data['telegram_id']])
    await message.answer(fmt.text(
        fmt.text('Пользователь', fmt.hitalic(user_data["name_user"]),'добавлен.'),
        fmt.text('Выберете команду:'),
        sep='\n'
    ),parse_mode="HTML",reply_markup=kb_a)
    await state.finish()
    await message.delete()    


async def remove_user_start(message: types.Message):
    await message.answer("Введите телеграм ID пользователя:", reply_markup=kb_cncl)
    await RemoveUser.input_id_for_remove.set()
    await message.delete()


async def remove_user(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Телеграм ID состоят только из цифр.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        await message.delete()
        return
    await state.update_data(telegram_id=message.text)
    user_data = await state.get_data()
    try:
        s.remove_user(user_data['telegram_id'])
    except:
        s.remove_user(user_data['telegram_id'])
    await message.answer(fmt.text(
        fmt.text('Пользователь с ID',fmt.hbold(str(user_data["telegram_id"])),'удален.'),
        fmt.text(fmt.hitalic('Выберете команду.')),
        sep='\n'),parse_mode="HTML",reply_markup=kb_a)
    await state.finish()        
    await message.delete()


async def add_admin_rights_start(message: types.Message):
    await message.answer("Введите телеграм ID пользователя:", reply_markup=kb_cncl)
    await AdminRights.input_id_for_add.set()
    await message.delete()


async def add_admin_rights(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Телеграм ID состоят только из цифр.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        await message.delete()
        return
    input_id = message.text
    if not input_id in s.get_append_id():
        await message.answer("Пользователя с таким Телеграм ID нет.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        await message.delete()
        return
    await state.update_data(telegram_id=input_id)
    user_data = await state.get_data()
    try:
        s.add_admin_rights(user_data['telegram_id'])
    except:
        s.add_admin_rights(user_data['telegram_id'])
    await message.answer(fmt.text(
        fmt.text('Пользователю с ID',fmt.hbold(str(user_data["telegram_id"])),'были добавлены права администратора.'),
        fmt.text('Выберете команду:'),
        sep='\n'),parse_mode="HTML",reply_markup=kb_a)
    await state.finish()        
    await message.delete()

async def remove_admin_rights_start(message: types.Message):
    await message.answer("Введите телеграм ID пользователя:", reply_markup=kb_cncl)
    await AdminRights.input_id_for_remove.set()
    await message.delete()


async def remove_admin_rights(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.delete()
        await message.answer("Телеграм ID состоят только из цифр.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        return
    input_id = message.text
    if not input_id in s.get_append_id():
        await message.delete()
        await message.answer("Пользователя с таким Телеграм ID нет.\nПроверьте вводимые данные.", reply_markup=kb_cncl)
        return
    await state.update_data(telegram_id=input_id)
    user_data = await state.get_data()
    try:
        s.remove_admin_rights(user_data['telegram_id'])
    except:
        s.remove_admin_rights(user_data['telegram_id'])
    await message.answer(fmt.text(
        fmt.text('У пользователя с ID',fmt.hbold(str(user_data["telegram_id"])),'были удалены права администратора.'),
        fmt.text('Выберете команду:'),
        sep='\n'),parse_mode="HTML",reply_markup=kb_a)
    await state.finish()        


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(fmt.text(
        fmt.text(fmt.hitalic('Выберете команду.')),
        sep='\n'
    ),parse_mode="HTML",reply_markup=kb_a)
    await message.delete()
    

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin_start,commands=['admin'],is_admin=True)
    dp.register_message_handler(add_user_start, Text(equals='Добавить пользователя', ignore_case=True),is_admin=True)
    dp.register_message_handler(add_name_user, state=AddUser.input_name_for_add,is_admin=True)
    dp.register_message_handler(add_telegram_id_user, state=AddUser.input_id_for_add,is_admin=True)
    dp.register_message_handler(remove_user_start, Text(equals='Удалить пользователя', ignore_case=True),is_admin=True)
    dp.register_message_handler(remove_user, state=RemoveUser.input_id_for_remove,is_admin=True)
    dp.register_message_handler(add_admin_rights_start, Text(equals='Добавить пользователю права администратора', ignore_case=True),is_admin=True)
    dp.register_message_handler(add_admin_rights, state=AdminRights.input_id_for_add,is_admin=True)
    dp.register_message_handler(add_admin_rights_start, Text(equals='Добавить пользователю права администратора', ignore_case=True),is_admin=True)
    dp.register_message_handler(add_admin_rights, state=AdminRights.input_id_for_add,is_admin=True)
    dp.register_message_handler(remove_admin_rights_start, Text(equals='Убрать у пользователя права администратора', ignore_case=True),is_admin=True)
    dp.register_message_handler(remove_admin_rights, state=AdminRights.input_id_for_remove,is_admin=True)
    dp.register_message_handler(not_admin_answer,commands=['admin'])






