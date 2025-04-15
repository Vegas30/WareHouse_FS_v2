# Импорт модуля для работы с PostgreSQL
import psycopg2
# Импорт модуля для логирования
import logging
# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import QMessageBox

class Database:
    """Класс для работы с базой данных PostgreSQL"""
    
    def __init__(self):
        """Инициализация соединения с базой данных"""
        try:
            # Установка соединения с базой данных PostgreSQL
            self.conn = psycopg2.connect(
                dbname="warehouse_fs",  # Имя базы данных
                user="postgres",        # Имя пользователя
                password="7773",        # Пароль
                host="localhost",       # Хост
                port="5432"             # Порт
            )
            # Создание курсора для выполнения запросов
            self.cursor = self.conn.cursor()
            # Логирование успешного подключения
            logging.info("Успешное подключение к базе данных")
        except Exception as e:
            # Логирование ошибки подключения
            logging.error(f"Ошибка подключения к базе данных: {str(e)}")
            raise

    def execute_query(self, query, params=None, parent_widget=None):
        """
        Выполнение SQL-запроса
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            parent_widget: Родительский виджет для отображения ошибок
            
        Returns:
            bool: Успешность выполнения запроса
        """
        try:
            # Выполнение SQL-запроса с параметрами
            self.cursor.execute(query, params or ())
            # Фиксация изменений в базе данных
            self.conn.commit()
            return True
        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"Ошибка базы данных: {str(e)}"
            # Логирование ошибки
            logging.error(error_msg)
            # Откат изменений в случае ошибки
            self.conn.rollback()
            
            # Отображение сообщения об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при выполнении операции:\n{error_msg}"
                )
            return False
            
    def fetch_all(self, query, params=None, parent_widget=None):
        """
        Получение всех результатов SQL-запроса
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            parent_widget: Родительский виджет для отображения ошибок
            
        Returns:
            list: Результаты запроса или пустой список в случае ошибки
        """
        try:
            # Выполнение SQL-запроса с параметрами
            self.cursor.execute(query, params or ())
            # Получение всех результатов
            return self.cursor.fetchall()
        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"Ошибка получения данных: {str(e)}"
            # Логирование ошибки
            logging.error(error_msg)
            
            # Отображение сообщения об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при получении данных:\n{error_msg}"
                )
            return []
            
    def fetch_one(self, query, params=None, parent_widget=None):
        """
        Получение одного результата SQL-запроса
        
        Args:
            query: SQL-запрос
            params: Параметры запроса
            parent_widget: Родительский виджет для отображения ошибок
            
        Returns:
            tuple: Результат запроса или None в случае ошибки
        """
        try:
            # Выполнение SQL-запроса с параметрами
            self.cursor.execute(query, params or ())
            # Получение одного результата
            return self.cursor.fetchone()
        except Exception as e:
            # Формирование сообщения об ошибке
            error_msg = f"Ошибка получения данных: {str(e)}"
            # Логирование ошибки
            logging.error(error_msg)
            
            # Отображение сообщения об ошибке, если указан родительский виджет
            if parent_widget:
                QMessageBox.critical(
                    parent_widget,
                    "Ошибка базы данных",
                    f"Произошла ошибка при получении данных:\n{error_msg}"
                )
            return None 

    def close(self):
        """Закрытие соединения с базой данных"""
        # Проверка наличия активного соединения
        if self.conn:
            # Закрытие курсора
            self.cursor.close()
            # Закрытие соединения
            self.conn.close()
            # Логирование закрытия соединения
            logging.info("Соединение с базой данных закрыто") 