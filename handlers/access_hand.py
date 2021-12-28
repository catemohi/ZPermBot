from aiogram import types, Dispatcher
from create_bot import bot


async def not_access(message: types.Message):
    await message.delete()
    markup = types.ReplyKeyboardRemove()
    await bot.send_message(message.from_user.id, 'У вас нет доступа.',reply_markup=markup)
    

def register_handlers_access(dp: Dispatcher):
    dp.register_message_handler(not_access,is_not_user=True)
