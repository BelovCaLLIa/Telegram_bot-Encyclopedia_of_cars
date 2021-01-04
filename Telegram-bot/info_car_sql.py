import sqlite3


class SQLighterCar:
    def __init__(self, database):
        """Подключаемся к БД с информацией о машинах и сохроняем соединение"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def export_model(self, id_car):
        """Возврат модели"""
        with self.connection:
            return self.cursor.execute("SELECT model FROM car WHERE id = ?", (id_car,)).fetchall()

    def export_photo_front(self, id_car):
        """Вывод фото машины"""
        with self.connection:
            return self.cursor.execute("SELECT foto_front_link FROM car WHERE id = ?", (id_car, )).fetchall()

    def export_text_about_car(self, id_car):
        """Вывод текста с инфой о машине"""
        with self.connection:
            return self.cursor.execute("SELECT info FROM car WHERE id = ?", (id_car,)).fetchall()

    def likes(self, model):
        """+1 к оценки машины"""
        with self.connection:
            self.cursor.execute("UPDATE car SET like_dynamics = like_dynamics + 1 WHERE model = ?", (model,)).fetchall()

    def dislikes(self, model):
        """-1 к оценки машины"""
        with self.connection:
            self.cursor.execute("UPDATE car SET like_dynamics = like_dynamics - 1 WHERE model = ?", (model,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
