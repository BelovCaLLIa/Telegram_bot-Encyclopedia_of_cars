import logging
import config
# Это библиотека аснхронная
# Класс бота, Dispatcher доставщик update, executor запускает бота
from aiogram import Bot, Dispatcher, executor, types

# Настроить ведение журнала
logging.basicConfig(level=logging.INFO)

# Инициализировать бота и диспетчера
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Этот обработчик будет вызываться, когда пользователь отправит команду /start или /help."""
    await message.reply("Hi!\nI'm EchoBot!")


# Доставка сообщений (Это дикоратор)
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


# Основнаю функция
if __name__ == '__main__':
    # Делает запросы get update к Telegram, доставляет нам сообщение
    executor.start_polling(dp, skip_updates=True)
