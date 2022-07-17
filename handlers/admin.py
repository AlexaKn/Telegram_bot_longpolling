from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# @dp.massage_handler(commamds=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Welcome, master!', reply_markup=admin_kb.button_case_admin)
    await message.delete()


# Начало загрузки нового товара
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.photo.set()
        await message.reply('Upload a photo')

# 1-й Ответ от пользователя и записываем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Enter a name')

# Второй ответ
# @dp.message_handler(state=FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('Enter a description')

# Третий ответ
# @dp.message_handler(state=FSMadmin.description)
async def load_description(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.next()
        await message.reply('Enter the price')

# Четвертый ответ
# @dp.message_handler(state=FSMadmin.price)
async def load_price(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()

# Отмена. Выход из машины состояний
# @dp.message_handler(state='*', commands='Cancel')
# @dp.message_handler(Text(equals='Cancel', ignore_case=True), state='*')
async def cancel_handler(message : types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

# @dp.callback_query_handler(lambda x: x.data and x.data.startswich('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} has been deleted.', show_alert=True)

# @dp.message_handler(commands='Delete')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nDescription: {ret[2]}\nPrice {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Delete{ret[1]}', callback_data=f'del {ret[1]}')))



def register_handlers_admin(dp : dispatcher):
    dp.register_message_handler(cm_start, commands=['Load'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(cancel_handler, state='*', commands='Cancel')
    dp.register_message_handler(cancel_handler, Text(equals='Cancel', ignore_case=True), state='*')
    dp.register_message_handler(make_changes_command, commands=['Moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswich('del '))
    dp.register_message_handler(delete_item, commands='Delete')