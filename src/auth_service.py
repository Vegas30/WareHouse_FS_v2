"""
Модуль аутентификации и управления пользователями.

Этот модуль предоставляет класс AuthService для аутентификации пользователей,
управления паролями и проверки прав доступа.

:author: Игорь Валуйсков
:version: 1.0
"""
# Импорт модуля для работы с PostgreSQL
import psycopg2
# Импорт класса для отображения диалоговых окон
from PyQt6.QtWidgets import QMessageBox
# Импорт модуля для логирования
import logging
# Импорт класса для работы с базой данных
from database import Database


class AuthService:
    """
    Класс для аутентификации и управления пользователями.
    
    Обеспечивает проверку учетных данных, смену пароля и проверку прав доступа.
    """

    @staticmethod
    def authenticate(username: str, password: str) -> tuple:
        """
        Метод аутентификации пользователя (упрощенный, без хеширования).
        
        :param username: Имя пользователя
        :type username: str
        :param password: Пароль пользователя
        :type password: str
            
        :returns: Кортеж (успех, полное имя, админ)
        :rtype: tuple[bool, str, bool]
        """
        try:
            # Создание подключения к базе данных
            db = Database()
            # SQL-запрос для получения данных пользователя
            db.cursor.execute(
                "SELECT password_hash, full_name, is_admin FROM users WHERE username = %s",
                (username,)
            )
            # Получение результата запроса
            result = db.cursor.fetchone()

            if result:
                # Распаковка данных пользователя
                db_password, full_name, is_admin = result
                # Проверка пароля (в продакшене должно использоваться хеширование)
                if password == db_password:
                    return True, full_name, is_admin

            # Возврат отрицательного результата
            return False, "", False
        except Exception as e:
            # Логирование ошибки аутентификации
            logging.error(f"Ошибка аутентификации: {str(e)}")
            return False, "", False

    @staticmethod
    def change_password(username: str, current_password: str, new_password: str) -> bool:
        """
        Изменение пароля пользователя (упрощенный метод, без хеширования).
        
        :param username: Имя пользователя
        :type username: str
        :param current_password: Текущий пароль
        :type current_password: str
        :param new_password: Новый пароль
        :type new_password: str
            
        :returns: Успешность изменения пароля
        :rtype: bool
        """
        try:
            # Создание подключения к базе данных
            db = Database()
            
            # Проверка текущего пароля
            db.cursor.execute(
                "SELECT 1 FROM users WHERE username = %s AND password_hash = %s",
                (username, current_password)
            )
            # Если текущий пароль неверный
            if not db.cursor.fetchone():
                return False

            # Обновление пароля в базе данных
            return db.execute_query(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (new_password, username)
            )
        except Exception as e:
            # Логирование ошибки изменения пароля
            logging.error(f"Ошибка изменения пароля: {str(e)}")
            return False

    def get_user_by_id(self, user_id):
        """
        Получение информации о пользователе по его ID.
        
        :param user_id: ID пользователя
        :type user_id: int
            
        :returns: Словарь с информацией о пользователе или None, если пользователь не найден
        :rtype: dict или None
        """
        try:
            # SQL-запрос для получения данных пользователя
            query = """
                SELECT user_id, username, full_name, is_admin, email
                FROM users
                WHERE user_id = %s
            """
            # Выполнение запроса
            result = self.db.fetch_one(query, (user_id,))
            
            if result:
                # Распаковка данных пользователя
                user_id, username, full_name, is_admin, email = result
                # Формирование словаря с данными пользователя
                return {
                    "user_id": user_id,
                    "username": username,
                    "full_name": full_name,
                    "is_admin": is_admin,
                    "email": email
                }
            return None
            
        except Exception as e:
            # Логирование ошибки получения данных пользователя
            logging.error(f"Ошибка получения данных пользователя: {str(e)}")
            return None
    
    def is_admin(self, user_id):
        """
        Проверка наличия прав администратора у пользователя.
        
        :param user_id: ID пользователя
        :type user_id: int
            
        :returns: True, если пользователь является администратором, иначе False
        :rtype: bool
        """
        # Получение данных пользователя
        user = self.get_user_by_id(user_id)
        # Проверка наличия прав администратора
        return user and user["is_admin"] 