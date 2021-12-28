from aiogram.utils import executor
from create_bot import dp
from handlers import contract_hand, general_hand,surcharges_hand,income_expenses_hand,admin_hand,access_hand
from aiogram import types


async def on_startup(dp):
    """
    Функция, запускающаяся во время страта бота.
    """
    #регистрация комманд бота
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
    ])
    #регистрация хендлеров
    access_hand.register_handlers_access(dp)
    contract_hand.register_handlers_contract(dp)
    income_expenses_hand.register_handlers_income_expenses(dp)
    surcharges_hand.register_handlers_surcharges(dp)
    admin_hand.register_handlers_admin(dp)
    general_hand.register_handlers(dp)
    

executor.start_polling(dp, skip_updates = True, on_startup=on_startup)

