# Для создания клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Создаём объект клавиатуры
menu = ReplyKeyboardMarkup(
    # Список списков с рядами кнопок
    keyboard=[
        [
            KeyboardButton(text="Случайный автомобиль 🎲")
        ],
        [
            KeyboardButton(text="🔥 ТОП-5 Красивых машин"),
            KeyboardButton(text="🔥 ТОП-5 Интересных машин")
        ],
        [
            KeyboardButton(text="🔥 ТОП-5 Машин группы B"),
            KeyboardButton(text="🔥 ТОП-5 Спортивных машин")
        ]
    ], resize_keyboard=True, one_time_keyboard=True)

# one_time_keyboard - одноразовае нажати
