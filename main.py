from aiogram.utils import executor
from creat_bot import dp
from Data_base import sqlite_db

async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_read()

from handlers import client, other, admin
client.register_handler_client(dp)
admin.register_handler_admin(dp)
other.register_handler_other(dp)



executor.start_polling(dp, skip_updates = True)
