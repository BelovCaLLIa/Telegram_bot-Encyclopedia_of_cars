# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    from bot import dp, on_startup, on_shutdown

    # Делает запросы get update к Telegram, доставляет нам сообщение
    # executor.start_polling(dp, skip_updates=True, on_shutdown=stop_bot)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
