from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Добавить пользователя')
b2 = KeyboardButton('Удалить пользователя')
b3 = KeyboardButton('Добавить пользователю права администратора')
b4 = KeyboardButton('Убрать у пользователя права администратора')
b5 = KeyboardButton('Назад')


kb_a = ReplyKeyboardMarkup(resize_keyboard=True)
kb_a.row(b1,b2)
kb_a.row(b3)
kb_a.row(b4)
kb_a.row(b5)
