from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Доходы/Расходы')
b2 = KeyboardButton('Доплаты')
b3 = KeyboardButton('Договоры')
kb_mm = ReplyKeyboardMarkup(resize_keyboard=True)
kb_mm.row(b1)
kb_mm.row(b2,b3)

