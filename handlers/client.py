from aiogram import types, dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from data_base import sqlite_db

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Have a good day!', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Please contact our consultant:\nhttps://t.me/Flowers_MarketBot')

# @dp.message_handler(commands=['Opening_hours'])
async def shop_open_hours(message: types.Message):
    await  bot.send_message(message.from_user.id, 'You can make an order from 8 am to 8 pm')

# @dp.message_handler(commands=['Delivery'])
async def delivery(message: types.Message):
    await bot.send_message(message.from_user.id, 'Round-the-clock delivery for free*\n*Free on the territory\
 of the city')

# @dp.message_handler(commands=['Shop'])
async def flowers_shop_command(message : types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(shop_open_hours, commands=['Opening_hours'])
    dp.register_message_handler(delivery, commands=['Delivery'])
    dp.register_message_handler(flowers_shop_command, commands=['Shop'])
