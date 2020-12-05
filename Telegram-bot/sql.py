# Для тг бота
import asyncio
# Для бд
import asyncpg
# Для дебага
import logging

from config import PG_USER, PG_PASS, HOST


# Настроить ведение журнала
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


# Создание таблицы 1 раз
async def create_db():
    # Открываем файл, читаем и подгружаем в переменныю
    create_db_command = open("users_db.sql", "r").read()

    logging.info("Connected to data base")
    # Создаём переменныю с подсказкой
    conn: asyncpg.Connection = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=HOST
    )
    # Выполнение команды
    await conn.execute(create_db_command)
    logging.info("Table has been created")
    # Закрываем соединение
    await conn.close()


# Создание пулла соединений для бота
# Возвращает соединение которое будет подкл. и откл.
async def create_pool():
    return await asyncpg.create_pool(
        user=PG_USER,
        password=PG_PASS,
        host=HOST
    )

# Если запустим только этот файл у нас выполниться только эта функция
# Создастся база
# При импорте этот код не выполниться
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
