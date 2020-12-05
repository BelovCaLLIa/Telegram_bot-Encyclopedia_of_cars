from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from bot import bot, dp, db


class DBCommands:
    pool: Connection = db
    # Команды SQL, которые мы будем использовать
    ADD_NEW_USER = "INSERT INTO users(chat_id,username,full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"

    # Функции, работающие с этими командами

    # Добавление нового пользователя
    async def add_new_user(self):
        # Получение пользователя из контекста
        # Смотрит кто ему написал
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        command = self.ADD_NEW_USER

        try:
            # self.pool это фактически DB
            # Возвращает id user-а
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            # То есть если пользователь уже добавлен, пропускаем
            pass

    # Считаем пользователей
    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    # Id пользователя
    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)


# Инициализируем класс
database = DBCommands()


# Приветствие Бота
@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await database.add_new_user()
    count_users = await database.count_users()
    text = ""

    # Если в id ошибка
    if not id:
        id = await database.get_id()
    else:
        text = "Записал в базу."

    # Ссылка на бота
    bot_username = (await bot.get_me()).username
    bot_link = "https://t.me/{bot_username}".format(
        bot_username=bot_username
    )
    text += f"""
Сейчас в базе {count_users} человек!
Ссылка на бота: {bot_link}
"""
    # Вывод пользователю
    await bot.send_message(chat_id, text)
