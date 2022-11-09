from aiogram import types, Dispatcher
from Keyboard.client_kb import kb_client
from creat_bot import bot
from aiogram.types import ReplyKeyboardRemove
from Data_base import sqlite_db


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую вас на нашем дилерском ', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:https://t.me/FenixAir_bot')


# @dp.message_handler(commands=['Режим_работы'])
async def dealer_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пн-пт с 9:00 до 21:00, Сб-Вс с 10:00 до 17:00')


# @dp.message_handler(commands=['Расположение'])
async def dealer_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пушкина, 61а', reply_markup=ReplyKeyboardRemove())


#@dp.message_handler(commands=['Меню'])
async def dealership_menu_command(message : types.Message):
    await sqlite_db.sql_read(message)


def register_handler_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(dealer_open_command, commands=['Режим_работы'])
    dp.register_message_handler(dealer_place_command, commands=['Расположение'])
    dp.register_message_handler(dealership_menu_command,commands=['Меню'])