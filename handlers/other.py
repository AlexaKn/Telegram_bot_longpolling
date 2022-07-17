from aiogram import types, dispatcher
from create_bot import dp
import json, string

# @dp.message_handler()
async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Swearing is prohibited by the rules')
        await message.delete()

def register_handlers_other(dp : dispatcher):
    dp.register_message_handler(echo_send)