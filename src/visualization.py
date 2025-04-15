# Импорт необходимых библиотек для работы с графиками
import matplotlib.pyplot as plt
# Импорт библиотеки для работы с данными
import pandas as pd
# Импорт библиотеки для работы с массивами и математическими операциями
import numpy as np
# Импорт необходимых компонентов из PyQt6 для создания графического интерфейса
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QDateEdit
# Импорт компонентов для работы со шрифтами
from PyQt6.QtGui import QFont
# Импорт базовых компонентов Qt
from PyQt6.QtCore import Qt, QDate
# Импорт компонента для встраивания графиков matplotlib в Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# Импорт класса Figure для создания фигур matplotlib
from matplotlib.figure import Figure
# Импорт модуля для работы с датами
import datetime
# Импорт модуля для работы с базой данных
from database import Database
# Импорт модуля для логирования
import logging

class ChartWidget(QWidget):
    """Базовый виджет для отображения графиков"""
    
    def __init__(self, parent=None):
        # Инициализация родительского класса
        super().__init__(parent)
        # Создание экземпляра базы данных
        self.db = Database()
        # Настройка пользовательского интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание вертикального layout для виджета
        self.layout = QVBoxLayout(self)
        
        # Создание фигуры matplotlib с заданными размерами и разрешением
        self.figure = Figure(figsize=(8, 6), dpi=100)
        # Создание холста для отображения графика
        self.canvas = FigureCanvas(self.figure)
        # Добавление холста в layout
        self.layout.addWidget(self.canvas)
        
        # Очистка графика при инициализации
        self.clear_plot()
    
    def clear_plot(self):
        """Очистка графика"""
        # Очистка текущей фигуры
        self.figure.clear()
        # Добавление новых осей на фигуру
        self.axes = self.figure.add_subplot(111)
        # Обновление холста для отображения изменений
        self.canvas.draw()
    
    def plot_bar_chart(self, x_data, y_data, title="", x_label="", y_label=""):
        """
        Построение столбчатой диаграммы
        
        Args:
            x_data: Данные для оси X
            y_data: Данные для оси Y
            title: Заголовок графика
            x_label: Подпись оси X
            y_label: Подпись оси Y
        """
        # Очистка текущего графика
        self.clear_plot()
        
        # Построение столбчатой диаграммы
        self.axes.bar(x_data, y_data)
        # Установка заголовка графика
        self.axes.set_title(title)
        # Установка подписи оси X
        self.axes.set_xlabel(x_label)
        # Установка подписи оси Y
        self.axes.set_ylabel(y_label)
        
        # Автоматический поворот меток на оси X, если их много
        if len(x_data) > 5:
            plt.setp(self.axes.get_xticklabels(), rotation=45, ha='right')
        
        # Оптимизация расположения элементов графика
        self.figure.tight_layout()
        # Обновление холста
        self.canvas.draw()
    
    def plot_pie_chart(self, data, labels, title=""):
        """
        Построение круговой диаграммы
        
        Args:
            data: Данные для секторов
            labels: Метки для секторов
            title: Заголовок графика
        """
        # Очистка текущего графика
        self.clear_plot()
        
        # Проверка, что все значения неотрицательные
        if any(d < 0 for d in data):
            raise ValueError("Data for pie chart must be non-negative")
        
        # Построение круговой диаграммы с процентами
        self.axes.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        # Установка заголовка графика
        self.axes.set_title(title)
        # Установка равных осей для круглой формы диаграммы
        self.axes.axis('equal')
        
        # Оптимизация расположения элементов графика
        self.figure.tight_layout()
        # Обновление холста
        self.canvas.draw()
    
    def plot_line_chart(self, x_data, y_data, title="", x_label="", y_label=""):
        """
        Построение линейного графика
        
        Args:
            x_data: Данные для оси X
            y_data: Данные для оси Y
            title: Заголовок графика
            x_label: Подпись оси X
            y_label: Подпись оси Y
        """
        # Очистка текущего графика
        self.clear_plot()
        
        # Построение линейного графика с маркерами
        self.axes.plot(x_data, y_data, marker='o')
        # Установка заголовка графика
        self.axes.set_title(title)
        # Установка подписи оси X
        self.axes.set_xlabel(x_label)
        # Установка подписи оси Y
        self.axes.set_ylabel(y_label)
        
        # Автоматический поворот меток на оси X, если их много
        if len(x_data) > 5:
            plt.setp(self.axes.get_xticklabels(), rotation=45, ha='right')
        
        # Оптимизация расположения элементов графика
        self.figure.tight_layout()
        # Обновление холста
        self.canvas.draw()


class InventoryAnalysisDialog(QDialog):
    """Диалог для анализа запасов и визуализации данных"""
    
    def __init__(self, parent=None):
        # Инициализация родительского класса
        super().__init__(parent)
        # Создание экземпляра базы данных
        self.db = Database()
        # Установка заголовка окна
        self.setWindowTitle("Анализ запасов")
        # Установка размеров окна
        self.resize(900, 700)
        # Настройка пользовательского интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание вертикального layout для диалога
        self.layout = QVBoxLayout(self)
        
        # Создание и настройка заголовка
        self.title_label = QLabel("Анализ и прогнозирование запасов")
        # Установка шрифта для заголовка
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Выравнивание заголовка по центру
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Добавление заголовка в layout
        self.layout.addWidget(self.title_label)
        
        # Настройка панели фильтров
        self.setup_filters()
        
        # Создание виджета для графиков
        self.chart_widget = ChartWidget(self)
        # Добавление виджета графиков в layout
        self.layout.addWidget(self.chart_widget)
        
        # Настройка кнопок анализа
        self.setup_buttons()
        
        # Загрузка данных по умолчанию
        self.update_stock_by_category()
    
    def setup_filters(self):
        """Настройка панели фильтров"""
        # Создание выпадающего списка для категорий
        self.category_combo = QComboBox(self)
        # Добавление пункта "Все категории"
        self.category_combo.addItem("Все категории")
        # Загрузка доступных категорий из базы данных
        try:
            categories = self.db.fetch_all(
                "SELECT DISTINCT category FROM products ORDER BY category",
                parent_widget=self
            )
            # Добавление категорий в выпадающий список
            for category in categories:
                self.category_combo.addItem(category[0])
        except Exception as e:
            # Логирование ошибки при загрузке категорий
            logging.error(f"Error loading categories: {str(e)}")
        
        # Создание выпадающего списка для складов
        self.warehouse_combo = QComboBox(self)
        # Добавление пункта "Все склады"
        self.warehouse_combo.addItem("Все склады")
        # Загрузка доступных складов из базы данных
        try:
            warehouses = self.db.fetch_all(
                "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name",
                parent_widget=self
            )
            # Добавление складов в выпадающий список
            for warehouse_id, warehouse_name in warehouses:
                self.warehouse_combo.addItem(warehouse_name, warehouse_id)
        except Exception as e:
            # Логирование ошибки при загрузке складов
            logging.error(f"Error loading warehouses: {str(e)}")
        
        # Создание виджетов для выбора дат
        self.start_date = QDateEdit(self)
        # Установка начальной даты (месяц назад)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        # Включение всплывающего календаря
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit(self)
        # Установка конечной даты (текущая дата)
        self.end_date.setDate(QDate.currentDate())
        # Включение всплывающего календаря
        self.end_date.setCalendarPopup(True)
        
        # Создание layout для фильтров
        filters_layout = QVBoxLayout()
        # Добавление элементов управления фильтрами
        filters_layout.addWidget(QLabel("Категория:"))
        filters_layout.addWidget(self.category_combo)
        filters_layout.addWidget(QLabel("Склад:"))
        filters_layout.addWidget(self.warehouse_combo)
        filters_layout.addWidget(QLabel("Период с:"))
        filters_layout.addWidget(self.start_date)
        filters_layout.addWidget(QLabel("по:"))
        filters_layout.addWidget(self.end_date)
        
        # Добавление layout с фильтрами в основной layout
        self.layout.addLayout(filters_layout)
    
    def setup_buttons(self):
        """Настройка кнопок анализа"""
        # Создание layout для кнопок
        buttons_layout = QVBoxLayout()
        
        # Создание и настройка кнопок для различных видов анализа
        self.stock_by_category_btn = QPushButton("Запасы по категориям")
        # Подключение обработчика нажатия кнопки
        self.stock_by_category_btn.clicked.connect(self.update_stock_by_category)
        buttons_layout.addWidget(self.stock_by_category_btn)
        
        self.stock_by_warehouse_btn = QPushButton("Запасы по складам")
        self.stock_by_warehouse_btn.clicked.connect(self.update_stock_by_warehouse)
        buttons_layout.addWidget(self.stock_by_warehouse_btn)
        
        self.low_stock_btn = QPushButton("Товары с низким запасом")
        self.low_stock_btn.clicked.connect(self.show_low_stock_items)
        buttons_layout.addWidget(self.low_stock_btn)
        
        self.stock_forecast_btn = QPushButton("Прогноз запасов")
        self.stock_forecast_btn.clicked.connect(self.show_stock_forecast)
        buttons_layout.addWidget(self.stock_forecast_btn)
        
        # Добавление layout с кнопками в основной layout
        self.layout.addLayout(buttons_layout)
    
    def update_stock_by_category(self):
        """Обновление графика запасов по категориям"""
        try:
            # Инициализация фильтра по складу
            warehouse_filter = ""
            params = []
            
            # Проверка выбора конкретного склада
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            # SQL-запрос для получения данных о запасах по категориям
            query = f"""
                SELECT p.category, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE 1=1 {warehouse_filter}
                GROUP BY p.category
                ORDER BY total_stock DESC
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, params, self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            categories = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            # Построение графика
            self.chart_widget.plot_bar_chart(
                categories, 
                quantities, 
                "Распределение запасов по категориям", 
                "Категория", 
                "Количество"
            )
        except Exception as e:
            # Логирование ошибки при обновлении графика
            logging.error(f"Error updating stock by category: {str(e)}")
    
    def update_stock_by_warehouse(self):
        """Обновление графика запасов по складам"""
        try:
            # Инициализация фильтра по категории
            category_filter = ""
            params = []
            
            # Проверка выбора конкретной категории
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            # SQL-запрос для получения данных о запасах по складам
            query = f"""
                SELECT w.warehouse_name, SUM(s.quantity) as total_stock
                FROM warehouses w
                JOIN stock s ON w.warehouse_id = s.warehouse_id
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1 {category_filter}
                GROUP BY w.warehouse_name
                ORDER BY total_stock DESC
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, params, self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            warehouses = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            # Построение круговой диаграммы
            self.chart_widget.plot_pie_chart(
                quantities, 
                warehouses, 
                "Распределение запасов по складам"
            )
        except Exception as e:
            # Логирование ошибки при обновлении графика
            logging.error(f"Error updating stock by warehouse: {str(e)}")
    
    def show_low_stock_items(self):
        """Отображение товаров с низким уровнем запасов"""
        try:
            # Установка порога для низкого уровня запасов
            low_stock_threshold = 20
            
            # Инициализация фильтров
            warehouse_filter = ""
            category_filter = ""
            params = [low_stock_threshold]
            
            # Проверка выбора конкретного склада
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            # Проверка выбора конкретной категории
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            # SQL-запрос для получения товаров с низким уровнем запасов
            query = f"""
                SELECT p.product_name, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE s.quantity < %s {warehouse_filter} {category_filter}
                GROUP BY p.product_name
                ORDER BY total_stock
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, params, self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            products = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            # Построение столбчатой диаграммы
            self.chart_widget.plot_bar_chart(
                products, 
                quantities, 
                "Товары с низким уровнем запасов", 
                "Товар", 
                "Количество"
            )
        except Exception as e:
            # Логирование ошибки при отображении товаров с низким запасом
            logging.error(f"Error showing low stock items: {str(e)}")
    
    def show_stock_forecast(self):
        """Отображение прогноза запасов на основе исторических данных"""
        try:
            # Получение выбранного периода
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # Инициализация фильтров
            warehouse_filter = ""
            category_filter = ""
            params = [start_date, end_date]
            
            # Проверка выбора конкретного склада
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            # Проверка выбора конкретной категории
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            # SQL-запрос для получения текущих запасов
            current_stock_query = f"""
                SELECT p.category, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE 1=1 {warehouse_filter} {category_filter}
                GROUP BY p.category
                ORDER BY p.category
            """
            
            # SQL-запрос для получения данных о потреблении товаров
            consumption_query = f"""
                SELECT p.category, SUM(oi.quantity) as total_ordered
                FROM products p
                JOIN order_items oi ON p.product_id = oi.product_id
                JOIN orders o ON oi.order_id = o.order_id
                JOIN stock s ON p.product_id = s.product_id
                WHERE o.order_date BETWEEN %s AND %s {warehouse_filter} {category_filter}
                GROUP BY p.category
                ORDER BY p.category
            """
            
            # Выполнение запросов
            current_stock = self.db.fetch_all(current_stock_query, params[2:], self)
            consumption = self.db.fetch_all(consumption_query, params, self)
            
            # Проверка наличия результатов
            if not current_stock or not consumption:
                self.chart_widget.clear_plot()
                return
            
            # Подготовка данных для графика
            categories = []
            current_values = []
            forecast_values = []
            
            # Создание словаря с данными о потреблении
            consumption_dict = {row[0]: row[1] for row in consumption}
            
            # Расчет прогноза для каждой категории
            for category, stock in current_stock:
                categories.append(category)
                current_values.append(stock)
                
                # Получение потребления за период
                consumption_rate = consumption_dict.get(category, 0)
                
                # Расчет прогноза на следующий месяц
                forecast = max(0, stock - consumption_rate)
                forecast_values.append(forecast)
            
            # Очистка текущего графика
            self.chart_widget.clear_plot()
            
            # Подготовка данных для столбчатой диаграммы
            x = np.arange(len(categories))
            width = 0.35
            
            # Построение столбчатой диаграммы с текущими и прогнозируемыми запасами
            self.chart_widget.axes.bar(x - width/2, current_values, width, label='Текущий запас')
            self.chart_widget.axes.bar(x + width/2, forecast_values, width, label='Прогноз через месяц')
            
            # Настройка отображения графика
            self.chart_widget.axes.set_title('Прогноз запасов по категориям')
            self.chart_widget.axes.set_xlabel('Категория')
            self.chart_widget.axes.set_ylabel('Количество')
            self.chart_widget.axes.set_xticks(x)
            self.chart_widget.axes.set_xticklabels(categories)
            plt.setp(self.chart_widget.axes.get_xticklabels(), rotation=45, ha='right')
            self.chart_widget.axes.legend()
            
            # Оптимизация расположения элементов графика
            self.chart_widget.figure.tight_layout()
            # Обновление холста
            self.chart_widget.canvas.draw()
        except Exception as e:
            # Логирование ошибки при отображении прогноза
            logging.error(f"Error showing stock forecast: {str(e)}")


class SalesReportDialog(QDialog):
    """Диалог для отображения отчетов по продажам"""
    
    def __init__(self, parent=None):
        # Инициализация родительского класса
        super().__init__(parent)
        # Создание экземпляра базы данных
        self.db = Database()
        # Установка заголовка окна
        self.setWindowTitle("Отчеты по продажам")
        # Установка размеров окна
        self.resize(900, 700)
        # Настройка пользовательского интерфейса
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание вертикального layout для диалога
        self.layout = QVBoxLayout(self)
        
        # Создание и настройка заголовка
        self.title_label = QLabel("Отчеты по продажам и поставкам")
        # Установка шрифта для заголовка
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Выравнивание заголовка по центру
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Добавление заголовка в layout
        self.layout.addWidget(self.title_label)
        
        # Настройка панели фильтров
        self.setup_filters()
        
        # Создание виджета для графиков
        self.chart_widget = ChartWidget(self)
        # Добавление виджета графиков в layout
        self.layout.addWidget(self.chart_widget)
        
        # Настройка кнопок отчетов
        self.setup_buttons()
        
        # Загрузка данных по умолчанию
        self.show_sales_by_category()
    
    def setup_filters(self):
        """Настройка панели фильтров"""
        # Создание виджетов для выбора дат
        self.start_date = QDateEdit(self)
        # Установка начальной даты (три месяца назад)
        self.start_date.setDate(QDate.currentDate().addMonths(-3))
        # Включение всплывающего календаря
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit(self)
        # Установка конечной даты (текущая дата)
        self.end_date.setDate(QDate.currentDate())
        # Включение всплывающего календаря
        self.end_date.setCalendarPopup(True)
        
        # Создание layout для фильтров
        filters_layout = QVBoxLayout()
        # Добавление элементов управления фильтрами
        filters_layout.addWidget(QLabel("Период с:"))
        filters_layout.addWidget(self.start_date)
        filters_layout.addWidget(QLabel("по:"))
        filters_layout.addWidget(self.end_date)
        
        # Добавление layout с фильтрами в основной layout
        self.layout.addLayout(filters_layout)
    
    def setup_buttons(self):
        """Настройка кнопок отчетов"""
        # Создание layout для кнопок
        buttons_layout = QVBoxLayout()
        
        # Создание и настройка кнопок для различных видов отчетов
        self.sales_by_category_btn = QPushButton("Продажи по категориям")
        # Подключение обработчика нажатия кнопки
        self.sales_by_category_btn.clicked.connect(self.show_sales_by_category)
        buttons_layout.addWidget(self.sales_by_category_btn)
        
        self.sales_by_month_btn = QPushButton("Продажи по месяцам")
        self.sales_by_month_btn.clicked.connect(self.show_sales_by_month)
        buttons_layout.addWidget(self.sales_by_month_btn)
        
        self.sales_by_supplier_btn = QPushButton("Поставки по поставщикам")
        self.sales_by_supplier_btn.clicked.connect(self.show_sales_by_supplier)
        buttons_layout.addWidget(self.sales_by_supplier_btn)
        
        self.top_products_btn = QPushButton("Топ продуктов")
        self.top_products_btn.clicked.connect(self.show_top_products)
        buttons_layout.addWidget(self.top_products_btn)
        
        # Добавление layout с кнопками в основной layout
        self.layout.addLayout(buttons_layout)
    
    def show_sales_by_category(self):
        """Отображение продаж по категориям"""
        try:
            # Получение выбранного периода
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # SQL-запрос для получения данных о продажах по категориям
            query = """
                SELECT p.category, SUM(oi.total_price) as total_sales
                FROM products p
                JOIN order_items oi ON p.product_id = oi.product_id
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY p.category
                ORDER BY total_sales DESC
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            categories = [row[0] for row in result]
            sales = [row[1] for row in result]
            
            # Построение круговой диаграммы
            self.chart_widget.plot_pie_chart(
                sales, 
                categories, 
                f"Продажи по категориям ({start_date} - {end_date})"
            )
        except Exception as e:
            # Логирование ошибки при отображении продаж по категориям
            logging.error(f"Error showing sales by category: {str(e)}")
    
    def show_sales_by_month(self):
        """Отображение продаж по месяцам"""
        try:
            # Получение выбранного периода
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # SQL-запрос для получения данных о продажах по месяцам
            query = """
                SELECT TO_CHAR(o.order_date, 'YYYY-MM') as month, SUM(oi.total_price) as total_sales
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
                ORDER BY month
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            months = [row[0] for row in result]
            sales = [row[1] for row in result]
            
            # Построение линейного графика
            self.chart_widget.plot_line_chart(
                months, 
                sales, 
                "Динамика продаж по месяцам", 
                "Месяц", 
                "Сумма продаж"
            )
        except Exception as e:
            # Логирование ошибки при отображении продаж по месяцам
            logging.error(f"Error showing sales by month: {str(e)}")
    
    def show_sales_by_supplier(self):
        """Отображение поставок по поставщикам"""
        try:
            # Получение выбранного периода
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # SQL-запрос для получения данных о поставках по поставщикам
            query = """
                SELECT s.supplier_name, SUM(o.total_amount) as total_orders
                FROM suppliers s
                JOIN orders o ON s.supplier_id = o.supplier_id
                WHERE o.order_date BETWEEN %s AND %s AND o.status = 'доставлен'
                GROUP BY s.supplier_name
                ORDER BY total_orders DESC
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            suppliers = [row[0] for row in result]
            orders = [row[1] for row in result]
            
            # Построение столбчатой диаграммы
            self.chart_widget.plot_bar_chart(
                suppliers, 
                orders, 
                f"Поставки по поставщикам ({start_date} - {end_date})", 
                "Поставщик", 
                "Сумма заказов"
            )
        except Exception as e:
            # Логирование ошибки при отображении поставок по поставщикам
            logging.error(f"Error showing sales by supplier: {str(e)}")
    
    def show_top_products(self):
        """Отображение топ-продуктов по продажам"""
        try:
            # Получение выбранного периода
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # Установка лимита по количеству товаров
            limit = 10
            
            # SQL-запрос для получения данных о топ-продуктах
            query = """
                SELECT p.product_name, SUM(oi.quantity) as total_quantity
                FROM products p
                JOIN order_items oi ON p.product_id = oi.product_id
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY p.product_name
                ORDER BY total_quantity DESC
                LIMIT %s
            """
            
            # Выполнение запроса
            result = self.db.fetch_all(query, (start_date, end_date, limit), self)
            
            # Проверка наличия результатов
            if not result:
                self.chart_widget.clear_plot()
                return
            
            # Извлечение данных для графика
            products = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            # Построение столбчатой диаграммы
            self.chart_widget.plot_bar_chart(
                products, 
                quantities, 
                f"Топ-{limit} продаваемых товаров ({start_date} - {end_date})", 
                "Товар", 
                "Количество"
            )
        except Exception as e:
            # Логирование ошибки при отображении топ-продуктов
            logging.error(f"Error showing top products: {str(e)}") 