import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохроняем соединение"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Все подписчики бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM subscriptions WHERE status = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем есть ли пользователь в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subscriptions WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, username, full_name, status=True):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO subscriptions (user_id, username, full_name, status) VALUES(?,?,?,?)",
                                       (user_id, username, full_name, status))

    def update_subscription(self, user_id, status):
        """Обновление статуса подписки"""
        with self.connection:
            return self.cursor.execute("UPDATE subscriptions SET status = ? WHERE user_id = ?", (status, user_id))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
