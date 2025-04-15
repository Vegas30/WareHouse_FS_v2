# Импорт модуля для работы с CSV файлами
import csv
# Импорт модуля для работы с JSON
import json
# Импорт библиотеки для работы с данными
import pandas as pd
# Импорт модуля для работы с операционной системой
import os
# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import QFileDialog, QMessageBox
# Импорт класса для работы с базой данных
from database import Database
# Импорт модуля для логирования
import logging
# Импорт модуля для работы с датами
import datetime

class DataExporter:
    """Класс для экспорта данных из приложения в различные форматы"""
    
    def __init__(self, parent_widget=None):
        """
        Инициализация экспортера данных
        
        Args:
            parent_widget: Родительский виджет для диалогов
        """
        # Создание объекта базы данных
        self.db = Database()
        # Сохранение ссылки на родительский виджет
        self.parent = parent_widget
    
    def export_to_csv(self, query, params=None, filename=None, headers=None):
        """
        Экспорт данных в CSV файл
        
        Args:
            query: SQL запрос для получения данных
            params: Параметры запроса
            filename: Имя файла для экспорта (если None, будет показан диалог)
            headers: Заголовки столбцов (если None, будут использованы имена полей)
            
        Returns:
            bool: Успешность экспорта
        """
        try:
            # Получение данных из базы данных
            data = self.db.fetch_all(query, params, self.parent)
            # Проверка наличия данных для экспорта
            if not data:
                # Показать предупреждение, если данных нет
                QMessageBox.warning(self.parent, "Экспорт данных", "Нет данных для экспорта")
                return False
            
            # Если имя файла не указано, запрашиваем его через диалог
            if not filename:
                # Формирование имени файла по умолчанию с текущей датой и временем
                default_name = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                # Отображение диалога сохранения файла
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent,
                    "Экспорт данных в CSV",
                    default_name,
                    "CSV Files (*.csv)"
                )
                # Проверка, не отменил ли пользователь диалог
                if not filename:
                    return False
            
            # Открытие файла для записи
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Создание объекта для записи в CSV
                writer = csv.writer(csvfile)
                
                # Запись заголовков, если они указаны
                if headers:
                    writer.writerow(headers)
                
                # Запись данных построчно
                for row in data:
                    writer.writerow(row)
            
            # Показать сообщение об успешном экспорте
            QMessageBox.information(
                self.parent, 
                "Экспорт данных", 
                f"Данные успешно экспортированы в файл {filename}"
            )
            return True
            
        except Exception as e:
            # Логирование ошибки экспорта
            error_msg = f"Ошибка при экспорте данных в CSV: {str(e)}"
            logging.error(error_msg)
            # Показать сообщение об ошибке
            QMessageBox.critical(self.parent, "Ошибка экспорта", error_msg)
            return False
    
    def export_to_excel(self, query, params=None, filename=None, sheet_name="Data", headers=None):
        """
        Экспорт данных в Excel файл
        
        Args:
            query: SQL запрос для получения данных
            params: Параметры запроса
            filename: Имя файла для экспорта (если None, будет показан диалог)
            sheet_name: Имя листа в Excel файле
            headers: Заголовки столбцов (если None, будут использованы имена полей)
            
        Returns:
            bool: Успешность экспорта
        """
        try:
            # Получение данных из базы данных
            data = self.db.fetch_all(query, params, self.parent)
            # Проверка наличия данных для экспорта
            if not data:
                # Показать предупреждение, если данных нет
                QMessageBox.warning(self.parent, "Экспорт данных", "Нет данных для экспорта")
                return False
            
            # Если имя файла не указано, запрашиваем его через диалог
            if not filename:
                # Формирование имени файла по умолчанию с текущей датой и временем
                default_name = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                # Отображение диалога сохранения файла
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent,
                    "Экспорт данных в Excel",
                    default_name,
                    "Excel Files (*.xlsx)"
                )
                # Проверка, не отменил ли пользователь диалог
                if not filename:
                    return False
            
            # Создание DataFrame из полученных данных
            df = pd.DataFrame(data)
            
            # Установка заголовков, если они указаны
            if headers:
                df.columns = headers
            
            # Сохранение данных в Excel файл
            df.to_excel(filename, sheet_name=sheet_name, index=False)
            
            # Показать сообщение об успешном экспорте
            QMessageBox.information(
                self.parent, 
                "Экспорт данных", 
                f"Данные успешно экспортированы в файл {filename}"
            )
            return True
            
        except Exception as e:
            # Логирование ошибки экспорта
            error_msg = f"Ошибка при экспорте данных в Excel: {str(e)}"
            logging.error(error_msg)
            # Показать сообщение об ошибке
            QMessageBox.critical(self.parent, "Ошибка экспорта", error_msg)
            return False


class DataImporter:
    """Класс для импорта данных в приложение из различных форматов"""
    
    def __init__(self, parent_widget=None):
        """
        Инициализация импортера данных
        
        Args:
            parent_widget: Родительский виджет для диалогов
        """
        # Создание объекта базы данных
        self.db = Database()
        # Сохранение ссылки на родительский виджет
        self.parent = parent_widget
    
    def import_from_csv(self, table_name, filename=None, delimiter=','):
        """
        Импорт данных из CSV файла
        
        Args:
            table_name: Имя таблицы для импорта
            filename: Имя файла для импорта (если None, будет показан диалог)
            delimiter: Разделитель в CSV файле
            
        Returns:
            bool: Успешность импорта
        """
        try:
            # Если имя файла не указано, запрашиваем его через диалог
            if not filename:
                # Отображение диалога выбора файла
                filename, _ = QFileDialog.getOpenFileName(
                    self.parent,
                    "Импорт данных из CSV",
                    "",
                    "CSV Files (*.csv)"
                )
                # Проверка, не отменил ли пользователь диалог
                if not filename:
                    return False
            
            # Открытие файла для чтения
            with open(filename, 'r', encoding='utf-8') as csvfile:
                # Создание объекта для чтения CSV
                csv_reader = csv.reader(csvfile, delimiter=delimiter)
                # Чтение заголовков
                headers = next(csv_reader)

                # Определение заголовков в зависимости от таблицы
                if table_name == "products":  # Товары
                    headers = ["product_name", "product_description", "category", "unit_price"]
                elif table_name == "stock":  # Запасы
                    headers = ["stock_id", "product_id", "warehouse_id", "quantity"]
                elif table_name == "orders":  # Заказы
                    headers = ["order_id", "order_date", "supplier_id", "total_amount", "status"]
                elif table_name == "suppliers":  # Поставщики
                    headers = ["supplier_id", "supplier_name", "contact_person", "phone_number", "email"]
                elif table_name == "warehouses":  # Склады
                    headers = ["warehouse_id", "warehouse_name", "location", "capacity"]
                
                # Формирование SQL-запроса для вставки данных
                placeholders = ', '.join(['%s'] * len(headers))
                columns = ', '.join(headers)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Импорт данных построчно
                for row in csv_reader:
                    values = row
                    self.db.execute_query(query, values, self.parent)
            
            # Показать сообщение об успешном импорте
            QMessageBox.information(
                self.parent, 
                "Импорт данных", 
                f"Данные успешно импортированы из файла {filename}"
            )
            return True
            
        except Exception as e:
            # Логирование ошибки импорта
            error_msg = f"Ошибка при импорте данных из CSV: {str(e)}"
            logging.error(error_msg)
            # Показать сообщение об ошибке
            QMessageBox.critical(self.parent, "Ошибка импорта", error_msg)
            return False
    
    def import_from_excel(self, table_name, filename=None, sheet_name=0):
        """
        Импорт данных из Excel файла
        
        Args:
            table_name: Имя таблицы для импорта
            filename: Имя файла для импорта (если None, будет показан диалог)
            sheet_name: Имя или индекс листа в Excel файле
            
        Returns:
            bool: Успешность импорта
        """
        try:
            # Если имя файла не указано, запрашиваем его через диалог
            if not filename:
                # Отображение диалога выбора файла
                filename, _ = QFileDialog.getOpenFileName(
                    self.parent,
                    "Импорт данных из Excel",
                    "",
                    "Excel Files (*.xlsx *.xls)"
                )
                # Проверка, не отменил ли пользователь диалог
                if not filename:
                    return False
            
            # Чтение данных из Excel файла
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            # Определение заголовков в зависимости от таблицы
            if table_name == "products":  # Товары
                headers = ["product_name", "product_description", "category", "unit_price"]
            elif table_name == "stock":  # Запасы
                headers = ["stock_id", "product_id", "warehouse_id", "quantity"]
            elif table_name == "orders":  # Заказы
                headers = ["order_id", "order_date", "supplier_id", "total_amount", "status"]
            elif table_name == "suppliers":  # Поставщики
                headers = ["supplier_id", "supplier_name", "contact_person", "phone_number", "email"]
            elif table_name == "warehouses":  # Склады
                headers = ["warehouse_id", "warehouse_name", "location", "capacity"]

            # Формирование SQL-запроса для вставки данных
            placeholders = ', '.join(['%s'] * len(headers))
            columns = ', '.join(headers)
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Импорт данных построчно
            for _, row in df.iterrows():
                values = row.tolist()
                self.db.execute_query(query, values, self.parent)
            
            # Показать сообщение об успешном импорте
            QMessageBox.information(
                self.parent, 
                "Импорт данных", 
                f"Данные успешно импортированы из файла {filename}"
            )
            return True
            
        except Exception as e:
            # Логирование ошибки импорта
            error_msg = f"Ошибка при импорте данных из Excel: {str(e)}"
            logging.error(error_msg)
            # Показать сообщение об ошибке
            QMessageBox.critical(self.parent, "Ошибка импорта", error_msg)
            return False 