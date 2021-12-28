from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Вчера')
b2 = KeyboardButton('Позавчера')
b3 = KeyboardButton('Сегодня')
b4 = KeyboardButton('Завтра')
b5 = KeyboardButton('Послезавтра')
b7 = KeyboardButton('Другой день')
b8 = KeyboardButton('Назад')
kb_ds = ReplyKeyboardMarkup(resize_keyboard=True)
kb_ds.row(b4,b5)
kb_ds.row(b3)
kb_ds.row(b1,b2)
kb_ds.row(b7,b8)