from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Сводная информация')
b2 = KeyboardButton('Движения средств')
b3 = KeyboardButton('Сводная информация и двежения средств')
b4 = KeyboardButton('Назад')
kb_ie = ReplyKeyboardMarkup(resize_keyboard=True)
kb_ie.row(b1,b2)
kb_ie.row(b3)
kb_ie.row(b4)
