from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from creat_bot import bot
from Data_base import sqlite_db
from Keyboard import admin_kb

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    engine = State()
    description = State()
    price = State()

#Получаем ID текущего модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_commands(message: types.Message):
    global ID
    ID = message.from_user == ID
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
    await message.delete()


#Начало диалога загрузки нового пункта меню
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

#Выход из состояний
#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async  def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

# Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply('Теперь введи название')

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['text'] = message.text
            await FSMAdmin.next()
            await message.reply('Введи объем')
#@dp.message_handler(state=FSMAdmin.engine)
async def load_engine(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['float'] = float(message.text)
            await FSMAdmin.next()
            await message.reply('введи описание')
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
            await FSMAdmin.next()
            await message.reply('Теперь укажите цену')
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] =float(message.text)
        await sqlite_db.sql_add_commandas(state)
        await state.finish()

#Регистрируем хендлеры
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена' )
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'],state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_engine, state=FSMAdmin.engine)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price,state=FSMAdmin.price)
    dp.register_message_handler(make_changes_commands, commands=['moderator'], is_chat_admin=True)