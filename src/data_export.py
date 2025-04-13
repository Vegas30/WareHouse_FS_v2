import csv
import json
import pandas as pd
import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from database import Database
import logging
import datetime

class DataExporter:
    """Класс для экспорта данных из приложения в различные форматы"""
    
    def __init__(self, parent_widget=None):
        """
        Инициализация экспортера данных
        
        Args:
            parent_widget: Родительский виджет для диалогов
        """
        self.db = Database()
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
            # Получаем данные
            data = self.db.fetch_all(query, params, self.parent)
            if not data:
                QMessageBox.warning(self.parent, "Экспорт данных", "Нет данных для экспорта")
                return False
            
            # Если имя файла не указано, запрашиваем через диалог
            if not filename:
                default_name = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent,
                    "Экспорт данных в CSV",
                    default_name,
                    "CSV Files (*.csv)"
                )
                if not filename:  # Пользователь отменил диалог
                    return False
            
            # Записываем данные в CSV файл
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Записываем заголовки, если указаны
                if headers:
                    writer.writerow(headers)
                
                # Записываем данные
                for row in data:
                    writer.writerow(row)
            
            QMessageBox.information(
                self.parent, 
                "Экспорт данных", 
                f"Данные успешно экспортированы в файл {filename}"
            )
            return True
            
        except Exception as e:
            error_msg = f"Ошибка при экспорте данных в CSV: {str(e)}"
            logging.error(error_msg)
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
            # Получаем данные
            data = self.db.fetch_all(query, params, self.parent)
            if not data:
                QMessageBox.warning(self.parent, "Экспорт данных", "Нет данных для экспорта")
                return False
            
            # Если имя файла не указано, запрашиваем через диалог
            if not filename:
                default_name = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent,
                    "Экспорт данных в Excel",
                    default_name,
                    "Excel Files (*.xlsx)"
                )
                if not filename:  # Пользователь отменил диалог
                    return False
            
            # Создаем DataFrame из данных
            df = pd.DataFrame(data)
            
            # Устанавливаем заголовки, если указаны
            if headers:
                df.columns = headers
            
            # Сохраняем в Excel
            df.to_excel(filename, sheet_name=sheet_name, index=False)
            
            QMessageBox.information(
                self.parent, 
                "Экспорт данных", 
                f"Данные успешно экспортированы в файл {filename}"
            )
            return True
            
        except Exception as e:
            error_msg = f"Ошибка при экспорте данных в Excel: {str(e)}"
            logging.error(error_msg)
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
        self.db = Database()
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
            # Если имя файла не указано, запрашиваем через диалог
            if not filename:
                filename, _ = QFileDialog.getOpenFileName(
                    self.parent,
                    "Импорт данных из CSV",
                    "",
                    "CSV Files (*.csv)"
                )
                if not filename:  # Пользователь отменил диалог
                    return False
            
            # Читаем данные из CSV файла
            with open(filename, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=delimiter)
                
                # Первая строка - заголовки
                headers = next(csv_reader)
                
                # Формируем запрос для вставки
                placeholders = ', '.join(['%s'] * len(headers))
                columns = ', '.join(headers)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                # Импортируем данные построчно
                for row in csv_reader:
                    self.db.execute_query(query, row, self.parent)
            
            QMessageBox.information(
                self.parent, 
                "Импорт данных", 
                f"Данные успешно импортированы из файла {filename}"
            )
            return True
            
        except Exception as e:
            error_msg = f"Ошибка при импорте данных из CSV: {str(e)}"
            logging.error(error_msg)
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
            # Если имя файла не указано, запрашиваем через диалог
            if not filename:
                filename, _ = QFileDialog.getOpenFileName(
                    self.parent,
                    "Импорт данных из Excel",
                    "",
                    "Excel Files (*.xlsx *.xls)"
                )
                if not filename:  # Пользователь отменил диалог
                    return False
            
            # Читаем данные из Excel файла
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            # Получаем заголовки и формируем запрос для вставки
            headers = df.columns.tolist()
            placeholders = ', '.join(['%s'] * len(headers))
            columns = ', '.join(headers)
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Импортируем данные построчно
            for _, row in df.iterrows():
                values = row.tolist()
                self.db.execute_query(query, values, self.parent)
            
            QMessageBox.information(
                self.parent, 
                "Импорт данных", 
                f"Данные успешно импортированы из файла {filename}"
            )
            return True
            
        except Exception as e:
            error_msg = f"Ошибка при импорте данных из Excel: {str(e)}"
            logging.error(error_msg)
            QMessageBox.critical(self.parent, "Ошибка импорта", error_msg)
            return False 