# Для создания клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создаём объект клавиатуры
menu = ReplyKeyboardMarkup(
    # Список списков с рядами кнопок
    keyboard=[
        [
            KeyboardButton(text="Случайный автомобиль")
        ],
        [
            KeyboardButton(text="ТОП-5 Красивых машин"),
            KeyboardButton(text="ТОП-5 Интересных машин")
        ]
    ], resize_keyboard=True)

