# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    from bot import dp

    # Делает запросы get update к Telegram, доставляет нам сообщение
    executor.start_polling(dp, skip_updates=True)
