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
from info_car_sql import SQLighterCar

import random
import time

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
db_car = SQLighterCar("info_car_db.db")

# Количество записей в БД
max_count_db = 60

# Старое рандомное число
old_rand = 0


# Генирация рандомного числа
def rand():
    # я знаю что так не очень хорошо делать, но как иначе?
    global old_rand
    shuffle = list(range(1, max_count_db + 1))
    # Перемешка элементов
    # random.shuffle(shuffle)
    random_value = random.choice(shuffle)
    if old_rand == random_value:
        rand()
    old_rand = random_value
    return random_value


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
    # Вывод информации в боте о машине
    value = rand()
    caption = db_car.export_text_about_car(value)
    file_photo = db_car.export_photo_front(value)
    # Многострадальные преобразования
    photo = open("".join(map(str, file_photo[0])), 'rb')
    await message.answer_photo(photo=photo, caption="".join(map(str, caption[0])), reply_markup=choice)


@dp.message_handler(Text(equals="ТОП-5 Красивых машин"))
async def beautiful_car(message: Message):
    # 5, 18, 26, 51, 52
    beautiful_cars_list = [5, 18, 26, 51, 52]
    for i in range(len(beautiful_cars_list)):
        caption = db_car.export_text_about_car(beautiful_cars_list[i])
        file_photo = db_car.export_photo_front(beautiful_cars_list[i])
        photo = open("".join(map(str, file_photo[0])), 'rb')
        await message.answer_photo(photo=photo, caption="".join(map(str, caption[0])), reply_markup=choice)
    # reply_markup=ReplyKeyboardRemove() - убирать кнопки


@dp.message_handler(Text(equals="ТОП-5 Интересных машин"))
async def interesting_car(message: Message):
    # 25, 26, 28, 46, 53
    interesting_cars = [25, 26, 28, 46, 53]
    for i in range(len(interesting_cars)):
        caption = db_car.export_text_about_car(interesting_cars[i])
        file_photo = db_car.export_photo_front(interesting_cars[i])
        photo = open("".join(map(str, file_photo[0])), 'rb')
        await message.answer_photo(photo=photo, caption="".join(map(str, caption[0])), reply_markup=choice)


@dp.message_handler(Text(equals="ТОП-5 Машин группы B"))
async def rally_car(message: Message):
    rally_cars = [10, 56, 55, 58, 57]
    for i in range(len(rally_cars)):
        caption = db_car.export_text_about_car(rally_cars[i])
        file_photo = db_car.export_photo_front(rally_cars[i])
        photo = open("".join(map(str, file_photo[0])), 'rb')
        await message.answer_photo(photo=photo, caption="".join(map(str, caption[0])), reply_markup=choice)


@dp.message_handler(Text(equals="ТОП-5 Спортивных машин"))
async def sport_car(message: Message):
    sport_cars = [1, 8, 30, 34, 35]
    for i in range(len(sport_cars)):
        caption = db_car.export_text_about_car(sport_cars[i])
        file_photo = db_car.export_photo_front(sport_cars[i])
        photo = open("".join(map(str, file_photo[0])), 'rb')
        await message.answer_photo(photo=photo, caption="".join(map(str, caption[0])), reply_markup=choice)


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
    # Смотрим что там в консоле
    logging.info(f"call = {callback_data}")
    db_car.likes(call.message.caption)
    await call.message.answer("Спасибо за лайк")
    await call.message.edit_reply_markup(reply_markup=None)


# Второй отлов нажатия дизлайка
@dp.callback_query_handler(like_callback.filter(emotion="dislike"))
async def dislike(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    db_car.dislikes(call.message.caption)
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
