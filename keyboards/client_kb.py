from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import ReplyKeyboardRemove

b1 = KeyboardButton('/Opening_hours')
b2 = KeyboardButton('/Delivery')
b3 = KeyboardButton('/Shop')
b4 = KeyboardButton('Give a phone number', request_contact=True)
b5 = KeyboardButton('Send location', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).insert(b3).row(b4, b5)
