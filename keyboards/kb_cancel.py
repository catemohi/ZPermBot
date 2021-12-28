from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Отмена')
kb_cncl = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cncl.add(b1)