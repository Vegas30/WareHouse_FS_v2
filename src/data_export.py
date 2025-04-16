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
# Импорт модулей для работы с PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
# Импорт для поддержки кириллицы
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

    def export_to_pdf(self, query, params=None, filename=None, headers=None, title="Отчет"):
        """
        Экспорт данных в PDF файл
        
        Args:
            query: SQL запрос для получения данных
            params: Параметры запроса
            filename: Имя файла для экспорта (если None, будет показан диалог)
            headers: Заголовки столбцов (если None, будут использованы имена полей)
            title: Заголовок документа
            
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
                default_name = f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                # Отображение диалога сохранения файла
                filename, _ = QFileDialog.getSaveFileName(
                    self.parent,
                    "Экспорт данных в PDF",
                    default_name,
                    "PDF Files (*.pdf)"
                )
                # Проверка, не отменил ли пользователь диалог
                if not filename:
                    return False
            
            # 1. Регистрация шрифтов (пробуем разные варианты для поддержки кириллицы)
            try:
                font_paths = [
                    os.path.join('src', 'fonts', 'DejaVuSans.ttf'),  # Ищем в папке src/fonts
                    'DejaVuSans.ttf',                               # Ищем в корне проекта
                    os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf'),  # Ищем относительно текущего файла
                ]
                
                font_registered = False
                font_name = 'Helvetica'  # Шрифт по умолчанию (без кириллицы)
                
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                        font_name = 'DejaVuSans'
                        font_registered = True
                        break
                
                if not font_registered:
                    try:
                        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
                        font_name = 'Arial'
                    except:
                        QMessageBox.warning(self.parent, "Предупреждение",
                                           "Не найден шрифт с поддержкой кириллицы. Возможны проблемы с отображением русских символов.")
            except Exception as e:
                logging.error(f"Ошибка при регистрации шрифта: {str(e)}")
                QMessageBox.warning(self.parent, "Предупреждение",
                                   "Не удалось зарегистрировать шрифт с поддержкой кириллицы. Возможны проблемы с отображением русских символов.")
            
            # Создание PDF документа с отступами
            page_width, page_height = A4
            margin = 2 * cm  # Отступ 2 см со всех сторон
            doc = SimpleDocTemplate(
                filename, 
                pagesize=A4, 
                leftMargin=margin,
                rightMargin=margin,
                topMargin=margin,
                bottomMargin=margin
            )
            
            # Элементы, которые будут добавлены в документ
            elements = []
            
            # Создание стилей с указанием нужных шрифтов
            styles = getSampleStyleSheet()
            # Переопределение стилей для использования шрифта с поддержкой кириллицы
            heading_style = styles['Heading1']
            heading_style.fontName = font_name
            
            # Создание стиля для текста в ячейках таблицы
            cell_style = ParagraphStyle(
                'CellStyle',
                fontName=font_name,
                fontSize=9,
                leading=12,  # Межстрочный интервал
                spaceAfter=6
            )
            
            # Добавление заголовка документа
            elements.append(Paragraph(title, heading_style))
            # Добавление отступа после заголовка
            elements.append(Spacer(1, 0.5 * cm))
            
            # Функция форматирования текста для ячеек
            def format_text(text, is_header=False):
                if is_header:
                    return Paragraph(f"<b>{text}</b>", cell_style)
                # Для обычного текста - просто создаем Paragraph для автопереноса
                return Paragraph(text, cell_style)
            
            # Подготовка данных для таблицы
            table_data = []
            
            # Добавление заголовков с форматированием
            if headers:
                formatted_headers = [format_text(header, True) for header in headers]
                table_data.append(formatted_headers)
            
            # Добавление данных с форматированием
            for row in data:
                formatted_row = []
                for item in row:
                    # Преобразование в строку и форматирование
                    item_str = str(item) if item is not None else ""
                    formatted_row.append(format_text(item_str))
                table_data.append(formatted_row)
            
            # Определение ширины страницы с учетом отступов
            available_width = page_width - (2 * margin)
            
            # Настройка ширины столбцов в зависимости от типа данных
            num_columns = len(table_data[0]) if table_data else 0
            
            if num_columns > 0:
                # Проверка, является ли это таблицей товаров
                is_products_table = False
                if headers and num_columns == 4:
                    product_headers = ["Название", "Описание", "Категория", "Цена"]
                    if all(h in headers for h in product_headers):
                        is_products_table = True
                
                if is_products_table:
                    # Оптимальное распределение для товаров: 25% для названия, 45% для описания, 15% для категории, 15% для цены
                    col_widths = [
                        available_width * 0.25,  # Название
                        available_width * 0.45,  # Описание
                        available_width * 0.15,  # Категория
                        available_width * 0.15   # Цена
                    ]
                else:
                    # Равномерное распределение для других таблиц
                    col_widths = [available_width / num_columns] * num_columns
                
                # Создание таблицы с заданной шириной столбцов и повторением заголовков
                table = Table(table_data, colWidths=col_widths, repeatRows=1)
                
                # Настройка стиля таблицы
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), font_name),  # Шрифт для заголовков
                    ('TOPPADDING', (0, 0), (-1, -1), 6),       # Отступ сверху в ячейках
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),    # Отступ снизу в ячейках
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),       # Выравнивание по верхнему краю
                    ('FONTNAME', (0, 1), (-1, -1), font_name), # Шрифт для данных
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),      # Отступ слева в ячейках
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),     # Отступ справа в ячейках
                ])
                
                # Применение стиля к таблице
                table.setStyle(style)
                
                # Добавление таблицы в документ
                elements.append(table)
            
            # Создание документа
            doc.build(elements)
            
            # Показать сообщение об успешном экспорте
            QMessageBox.information(
                self.parent, 
                "Экспорт данных", 
                f"Данные успешно экспортированы в файл {filename}"
            )
            return True
            
        except Exception as e:
            # Логирование ошибки экспорта
            error_msg = f"Ошибка при экспорте данных в PDF: {str(e)}"
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