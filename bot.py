import logging
import config
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import Command, CommandHelp, CommandStart, Text
# Класс бота, Dispatcher доставщик update, executor запускает бота
from aiogram import Bot, Dispatcher, types
# Импортируем созданные кнопки
from Keyboard import menu

# Настроить ведение журнала
logging.basicConfig(level=logging.INFO)

# Инициализировать бота и диспетчера
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


# Ответ на start
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Привет!")


# Ответ на help
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ['Список команд', '/start - Начать диалог', '/help - получить справку']
    await message.answer('\n'.join(text))


# Реакция на команду menu
@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Вы можете выбрать команду из меню ниже:", reply_markup=menu)


# Теперь нужно сделать handler для каждой кнопки
@dp.message_handler(Text(equals="Случайный автомобиль"))
async def random_car(message: Message):
    # Убираем кнопку
    await message.answer("Вы выброли 'Случайный автомобиль'", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="ТОП-5 Красивых машин"))
async def beautiful_car(message: Message):
    await message.answer("Вы выброли 'ТОП-5 Красивых машин'", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="ТОП-5 Интересных машин"))
async def interesting_car(message: Message):
    await message.answer("Вы выброли 'ТОП-5 Интересных машин'", reply_markup=ReplyKeyboardRemove())
