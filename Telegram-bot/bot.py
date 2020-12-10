import logging

# Класс бота, Dispatcher доставщик update, executor запускает бота
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.builtin import Command, CommandHelp, CommandStart, Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

import config
# Импортируем созданные кнопки
from Keyboard import menu
from inline import choice, like_callback

# Для бд
from users_sql import SQLighter

# Настроить ведение журнала
# Более удобная форма
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализировать бота и диспетчера
# parse_mode нужен для форматирования
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
# Передаём файл с бд
db = SQLighter("users_db.db")


# Ответ на start
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Привет!")


# Ответ на help
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ['Список команд',
            '/start - Начать диалог',
            '/menu - Получить список команд',
            '/remove - Убирает кнопки',
            '/subscribe - Подписаться на рассылку',
            '/unsubscribe - Отписаться от рассылки',
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


# Второй отлов нажатия дизлайка
@dp.callback_query_handler(like_callback.filter(emotion="dislike"))
async def dislike(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    await call.message.answer("Буду стараться")
    await call.message.edit_reply_markup(reply_markup=None)


# Команда активации подписки
@dp.message_handler(commands=["subscribe"])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # Если пользователя нет, то добавляем его
        db.add_subscriber(message.from_user.id, message.from_user.username, message.from_user.full_name)
    else:
        # Если он уже есть, то просто обнавляем статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer("Вы успешно подписались!")


# Команда отписки
@dp.message_handler(commands=["unsubscribe"])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # Если пользователя нет, то добавляем его с неактивной подпиской
        db.add_subscriber(message.from_user.id, message.from_user.username, message.from_user.full_name, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписались.")
