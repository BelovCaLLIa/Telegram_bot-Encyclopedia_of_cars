from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# CallbackData для работы с кнопками rating - это префикс
# parts - что мы будем сохронять в этой кнопке
like_callback = CallbackData("rating", "emotion", "quantity")


# choice = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Лайк", callback_data=like_collback.new(
#                 model_car="Opel", quantity=+1
#             )),
#             InlineKeyboardButton(text="Дизлайк", callback_data=""),
#         ],
#     ]
# )

choice = InlineKeyboardMarkup()

# like = InlineKeyboardButton(text="👍", callback_data=like_callback.new(
#     model_car="Opel", quantity=+1))

like = InlineKeyboardButton(text="👍", callback_data="rating:like:+1")
# Добавляем кнопку
choice.insert(like)

dislike = InlineKeyboardButton(text="👎", callback_data="rating:dislike:-1")
# Добавляем кнопку
choice.insert(dislike)
