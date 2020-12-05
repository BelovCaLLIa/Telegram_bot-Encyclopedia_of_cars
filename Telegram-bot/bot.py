# Позволяет установить всё в одну команду
# -pip install -r (имя этого файла)
# Нужные библиотеки для проекта:
# aiogram
# Для работы с БД PosgresSql:
# asyncpg
# python-dotenv

import asyncio
import logging
import config
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters.builtin import Command, CommandHelp, Text
# Класс бота, Dispatcher доставщик update, executor запускает бота
from aiogram import Bot, Dispatcher, types
# Импортируем созданные кнопки
from Keyboard import menu
from inline import choice, like_callback
# Sql
from sql import create_pool

# Настроить ведение журнала
# Более удобная форма
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализировать бота и диспетчера
# parse_mode нужен для форматирования
# bot = Bot(token=config.API_TOKEN)
# dp = Dispatcher(bot)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Соединение с БД create_pool()
loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())


# Ответ на start
# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     await message.answer("Привет!")


# Закрытие бота
async def stop_bot(db):
    await bot.close()


# Ответ на help
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ['Список команд',
            '/start - Начать диалог',
            '/menu - Получить список команд',
            '/remove - Убирает кнопки',
            '/help - Получить справку']
    await message.answer('\n'.join(text))


# Реакция на команду menu
@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Вы можете выбрать команду из меню ниже:", reply_markup=menu)


# Теперь нужно сделать handler для каждой кнопки
@dp.message_handler(Text(equals="Случайный автомобиль"))
async def random_car(message: Message):
    # Убираем кнопку
    await message.answer("Вы выброли 'Случайный автомобиль'", reply_markup=choice)


@dp.message_handler(Text(equals="ТОП-5 Красивых машин"))
async def beautiful_car(message: Message):
    await message.answer("Вы выброли 'ТОП-5 Красивых машин'", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="ТОП-5 Интересных машин"))
async def interesting_car(message: Message):
    await message.answer("Вы выброли 'ТОП-5 Интересных машин'", reply_markup=ReplyKeyboardRemove())


# Уберает кнопки
@dp.message_handler(Command("remove"))
async def remove(message: Message):
    await message.answer("Убераю кнопки", reply_markup=ReplyKeyboardRemove())


# Сюда попадает нажатие на inlite кнопку
# Все нажатия c параметром лайк
@dp.callback_query_handler(like_callback.filter(emotion="like"))
async def lick(call: CallbackQuery, callback_data: dict):
    # Убираем часики
    # Это более простая констукция
    await call.answer(cache_time=60)
    # Смотрим что там
    logging.info(f"call = {callback_data}")
    await call.message.answer("Спасибо за лайк")
    await call.message.edit_reply_markup(reply_markup=None)


# Второй, отлов нажатия дизлайка
@dp.callback_query_handler(like_callback.filter(emotion="dislike"))
async def dislike(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    await call.message.answer("Буду стараться")
    await call.message.edit_reply_markup(reply_markup=None)
