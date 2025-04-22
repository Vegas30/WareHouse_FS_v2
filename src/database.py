"""
Модуль для работы с базой данных PostgreSQL.

Этот модуль предоставляет класс Database для подключения к базе данных PostgreSQL
и выполнения запросов к ней в контексте приложения для управления складом.

:author: Игорь Валуйсков
:version: 1.0
"""
# Импорт модуля для работы с PostgreSQL
import psycopg2
# Импорт модуля для логирования
import logging
# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import QMessageBox

class Database:
    """
    Класс для работы с базой данных PostgreSQL.
    
    Обеспечивает соединение с базой данных и предоставляет методы
    для выполнения запросов и получения результатов.
    """
    
    def __init__(self):
        """
        Инициализация соединения с базой данных.
        
        Создает соединение с базой данных PostgreSQL используя
        заданные параметры подключения.
        
        :raises: Exception при ошибке подключения к базе данных
        """
        try:
            # Установка соединения с базой данных PostgreSQL
            self.conn = psycopg2.connect(
                dbname="test_db",  # Имя базы данных
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
        Выполнение SQL-запроса.
        
        :param query: SQL-запрос для выполнения
        :type query: str
        :param params: Параметры запроса
        :type params: tuple или None
        :param parent_widget: Родительский виджет для отображения ошибок
        :type parent_widget: QWidget или None
            
        :returns: Результат успешности выполнения запроса
        :rtype: bool
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
        Получение всех результатов SQL-запроса.
        
        :param query: SQL-запрос для выполнения
        :type query: str
        :param params: Параметры запроса
        :type params: tuple или None
        :param parent_widget: Родительский виджет для отображения ошибок
        :type parent_widget: QWidget или None
            
        :returns: Список результатов запроса или пустой список в случае ошибки
        :rtype: list
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
        Получение одного результата SQL-запроса.
        
        :param query: SQL-запрос для выполнения
        :type query: str
        :param params: Параметры запроса
        :type params: tuple или None
        :param parent_widget: Родительский виджет для отображения ошибок
        :type parent_widget: QWidget или None
            
        :returns: Результат запроса или None в случае ошибки
        :rtype: tuple или None
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
        """
        Закрытие соединения с базой данных.
        
        Закрывает курсор и соединение с базой данных, освобождая ресурсы.
        
        :returns: None
        """
        # Проверка наличия активного соединения
        if self.conn:
            # Закрытие курсора
            self.cursor.close()
            # Закрытие соединения
            self.conn.close()
            # Логирование закрытия соединения
            logging.info("Соединение с базой данных закрыто") 