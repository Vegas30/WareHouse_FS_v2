import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QDateEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from database import Database
import logging

class ChartWidget(QWidget):
    """Базовый виджет для отображения графиков"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.layout = QVBoxLayout(self)
        
        # Создаем фигуру matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Очищаем график
        self.clear_plot()
    
    def clear_plot(self):
        """Очистка графика"""
        self.figure.clear()
        # Добавляем оси
        self.axes = self.figure.add_subplot(111)
        # Обновляем холст
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
        self.clear_plot()
        
        self.axes.bar(x_data, y_data)
        self.axes.set_title(title)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        
        # Автоматический поворот меток на оси X, если их много
        if len(x_data) > 5:
            plt.setp(self.axes.get_xticklabels(), rotation=45, ha='right')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_pie_chart(self, data, labels, title=""):
        """
        Построение круговой диаграммы
        
        Args:
            data: Данные для секторов
            labels: Метки для секторов
            title: Заголовок графика
        """
        self.clear_plot()
        
        # Проверяем, что все значения неотрицательные
        if any(d < 0 for d in data):
            raise ValueError("Data for pie chart must be non-negative")
        
        self.axes.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        self.axes.set_title(title)
        self.axes.axis('equal')  # Круговая диаграмма выглядит лучше в круге
        
        self.figure.tight_layout()
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
        self.clear_plot()
        
        self.axes.plot(x_data, y_data, marker='o')
        self.axes.set_title(title)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        
        # Автоматический поворот меток на оси X, если их много
        if len(x_data) > 5:
            plt.setp(self.axes.get_xticklabels(), rotation=45, ha='right')
        
        self.figure.tight_layout()
        self.canvas.draw()


class InventoryAnalysisDialog(QDialog):
    """Диалог для анализа запасов и визуализации данных"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setWindowTitle("Анализ запасов")
        self.resize(900, 700)
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.layout = QVBoxLayout(self)
        
        # Заголовок
        self.title_label = QLabel("Анализ и прогнозирование запасов")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Панель фильтров
        self.setup_filters()
        
        # Виджет для графиков
        self.chart_widget = ChartWidget(self)
        self.layout.addWidget(self.chart_widget)
        
        # Кнопки анализа
        self.setup_buttons()
        
        # Загружаем данные по умолчанию
        self.update_stock_by_category()
    
    def setup_filters(self):
        """Настройка панели фильтров"""
        # Выбор категории товаров
        self.category_combo = QComboBox(self)
        self.category_combo.addItem("Все категории")
        # Загружаем доступные категории
        try:
            categories = self.db.fetch_all(
                "SELECT DISTINCT category FROM products ORDER BY category",
                parent_widget=self
            )
            for category in categories:
                self.category_combo.addItem(category[0])
        except Exception as e:
            logging.error(f"Error loading categories: {str(e)}")
        
        # Выбор склада
        self.warehouse_combo = QComboBox(self)
        self.warehouse_combo.addItem("Все склады")
        # Загружаем доступные склады
        try:
            warehouses = self.db.fetch_all(
                "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name",
                parent_widget=self
            )
            for warehouse_id, warehouse_name in warehouses:
                self.warehouse_combo.addItem(warehouse_name, warehouse_id)
        except Exception as e:
            logging.error(f"Error loading warehouses: {str(e)}")
        
        # Выбор периода
        self.start_date = QDateEdit(self)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit(self)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        # Добавляем фильтры на форму
        filters_layout = QVBoxLayout()
        filters_layout.addWidget(QLabel("Категория:"))
        filters_layout.addWidget(self.category_combo)
        filters_layout.addWidget(QLabel("Склад:"))
        filters_layout.addWidget(self.warehouse_combo)
        filters_layout.addWidget(QLabel("Период с:"))
        filters_layout.addWidget(self.start_date)
        filters_layout.addWidget(QLabel("по:"))
        filters_layout.addWidget(self.end_date)
        
        self.layout.addLayout(filters_layout)
    
    def setup_buttons(self):
        """Настройка кнопок анализа"""
        buttons_layout = QVBoxLayout()
        
        # Кнопки для различных видов анализа
        self.stock_by_category_btn = QPushButton("Запасы по категориям")
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
        
        self.layout.addLayout(buttons_layout)
    
    def update_stock_by_category(self):
        """Обновление графика запасов по категориям"""
        try:
            warehouse_filter = ""
            params = []
            
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            query = f"""
                SELECT p.category, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE 1=1 {warehouse_filter}
                GROUP BY p.category
                ORDER BY total_stock DESC
            """
            
            result = self.db.fetch_all(query, params, self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            categories = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            self.chart_widget.plot_bar_chart(
                categories, 
                quantities, 
                "Распределение запасов по категориям", 
                "Категория", 
                "Количество"
            )
        except Exception as e:
            logging.error(f"Error updating stock by category: {str(e)}")
    
    def update_stock_by_warehouse(self):
        """Обновление графика запасов по складам"""
        try:
            category_filter = ""
            params = []
            
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            query = f"""
                SELECT w.warehouse_name, SUM(s.quantity) as total_stock
                FROM warehouses w
                JOIN stock s ON w.warehouse_id = s.warehouse_id
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1 {category_filter}
                GROUP BY w.warehouse_name
                ORDER BY total_stock DESC
            """
            
            result = self.db.fetch_all(query, params, self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            warehouses = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            self.chart_widget.plot_pie_chart(
                quantities, 
                warehouses, 
                "Распределение запасов по складам"
            )
        except Exception as e:
            logging.error(f"Error updating stock by warehouse: {str(e)}")
    
    def show_low_stock_items(self):
        """Отображение товаров с низким уровнем запасов"""
        try:
            # Для примера считаем низким запасом менее 20 единиц
            low_stock_threshold = 20
            
            warehouse_filter = ""
            category_filter = ""
            params = [low_stock_threshold]
            
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            query = f"""
                SELECT p.product_name, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE s.quantity < %s {warehouse_filter} {category_filter}
                GROUP BY p.product_name
                ORDER BY total_stock
            """
            
            result = self.db.fetch_all(query, params, self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            products = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            self.chart_widget.plot_bar_chart(
                products, 
                quantities, 
                "Товары с низким уровнем запасов", 
                "Товар", 
                "Количество"
            )
        except Exception as e:
            logging.error(f"Error showing low stock items: {str(e)}")
    
    def show_stock_forecast(self):
        """Отображение прогноза запасов на основе исторических данных"""
        try:
            # Получаем исторические данные за выбранный период
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # Предполагаем, что у нас есть данные о продажах/расходе товаров в таблице заказов
            warehouse_filter = ""
            category_filter = ""
            params = [start_date, end_date]
            
            if self.warehouse_combo.currentIndex() > 0:
                warehouse_id = self.warehouse_combo.currentData()
                warehouse_filter = "AND s.warehouse_id = %s"
                params.append(warehouse_id)
            
            if self.category_combo.currentIndex() > 0:
                category = self.category_combo.currentText()
                category_filter = "AND p.category = %s"
                params.append(category)
            
            # Получаем данные о текущих запасах
            current_stock_query = f"""
                SELECT p.category, SUM(s.quantity) as total_stock
                FROM products p
                JOIN stock s ON p.product_id = s.product_id
                WHERE 1=1 {warehouse_filter} {category_filter}
                GROUP BY p.category
                ORDER BY p.category
            """
            
            # Получаем данные о потреблении товаров (на основе заказов)
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
            
            current_stock = self.db.fetch_all(current_stock_query, params[2:], self)
            consumption = self.db.fetch_all(consumption_query, params, self)
            
            if not current_stock or not consumption:
                self.chart_widget.clear_plot()
                return
            
            # Форматируем данные для графика
            categories = []
            current_values = []
            forecast_values = []
            
            # Создаем словарь с данными о потреблении
            consumption_dict = {row[0]: row[1] for row in consumption}
            
            # Для каждой категории вычисляем прогноз на следующий месяц
            for category, stock in current_stock:
                categories.append(category)
                current_values.append(stock)
                
                # Получаем потребление за период
                consumption_rate = consumption_dict.get(category, 0)
                
                # Прогнозируем запас через месяц (текущий запас - месячное потребление)
                forecast = max(0, stock - consumption_rate)
                forecast_values.append(forecast)
            
            # Строим столбчатую диаграмму с текущими и прогнозируемыми запасами
            self.chart_widget.clear_plot()
            
            x = np.arange(len(categories))
            width = 0.35
            
            self.chart_widget.axes.bar(x - width/2, current_values, width, label='Текущий запас')
            self.chart_widget.axes.bar(x + width/2, forecast_values, width, label='Прогноз через месяц')
            
            self.chart_widget.axes.set_title('Прогноз запасов по категориям')
            self.chart_widget.axes.set_xlabel('Категория')
            self.chart_widget.axes.set_ylabel('Количество')
            self.chart_widget.axes.set_xticks(x)
            self.chart_widget.axes.set_xticklabels(categories)
            plt.setp(self.chart_widget.axes.get_xticklabels(), rotation=45, ha='right')
            self.chart_widget.axes.legend()
            
            self.chart_widget.figure.tight_layout()
            self.chart_widget.canvas.draw()
        except Exception as e:
            logging.error(f"Error showing stock forecast: {str(e)}")


class SalesReportDialog(QDialog):
    """Диалог для отображения отчетов по продажам"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setWindowTitle("Отчеты по продажам")
        self.resize(900, 700)
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.layout = QVBoxLayout(self)
        
        # Заголовок
        self.title_label = QLabel("Отчеты по продажам и поставкам")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Панель фильтров
        self.setup_filters()
        
        # Виджет для графиков
        self.chart_widget = ChartWidget(self)
        self.layout.addWidget(self.chart_widget)
        
        # Кнопки отчетов
        self.setup_buttons()
        
        # Загружаем данные по умолчанию
        self.show_sales_by_category()
    
    def setup_filters(self):
        """Настройка панели фильтров"""
        # Выбор периода
        self.start_date = QDateEdit(self)
        self.start_date.setDate(QDate.currentDate().addMonths(-3))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit(self)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        # Добавляем фильтры на форму
        filters_layout = QVBoxLayout()
        filters_layout.addWidget(QLabel("Период с:"))
        filters_layout.addWidget(self.start_date)
        filters_layout.addWidget(QLabel("по:"))
        filters_layout.addWidget(self.end_date)
        
        self.layout.addLayout(filters_layout)
    
    def setup_buttons(self):
        """Настройка кнопок отчетов"""
        buttons_layout = QVBoxLayout()
        
        # Кнопки для различных видов отчетов
        self.sales_by_category_btn = QPushButton("Продажи по категориям")
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
        
        self.layout.addLayout(buttons_layout)
    
    def show_sales_by_category(self):
        """Отображение продаж по категориям"""
        try:
            # Получение данных за выбранный период
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            query = """
                SELECT p.category, SUM(oi.total_price) as total_sales
                FROM products p
                JOIN order_items oi ON p.product_id = oi.product_id
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY p.category
                ORDER BY total_sales DESC
            """
            
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            categories = [row[0] for row in result]
            sales = [row[1] for row in result]
            
            self.chart_widget.plot_pie_chart(
                sales, 
                categories, 
                f"Продажи по категориям ({start_date} - {end_date})"
            )
        except Exception as e:
            logging.error(f"Error showing sales by category: {str(e)}")
    
    def show_sales_by_month(self):
        """Отображение продаж по месяцам"""
        try:
            # Получение данных за выбранный период
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            query = """
                SELECT TO_CHAR(o.order_date, 'YYYY-MM') as month, SUM(oi.total_price) as total_sales
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
                ORDER BY month
            """
            
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            months = [row[0] for row in result]
            sales = [row[1] for row in result]
            
            self.chart_widget.plot_line_chart(
                months, 
                sales, 
                "Динамика продаж по месяцам", 
                "Месяц", 
                "Сумма продаж"
            )
        except Exception as e:
            logging.error(f"Error showing sales by month: {str(e)}")
    
    def show_sales_by_supplier(self):
        """Отображение поставок по поставщикам"""
        try:
            # Получение данных за выбранный период
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            query = """
                SELECT s.supplier_name, SUM(o.total_amount) as total_orders
                FROM suppliers s
                JOIN orders o ON s.supplier_id = o.supplier_id
                WHERE o.order_date BETWEEN %s AND %s AND o.status = 'доставлен'
                GROUP BY s.supplier_name
                ORDER BY total_orders DESC
            """
            
            result = self.db.fetch_all(query, (start_date, end_date), self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            suppliers = [row[0] for row in result]
            orders = [row[1] for row in result]
            
            self.chart_widget.plot_bar_chart(
                suppliers, 
                orders, 
                f"Поставки по поставщикам ({start_date} - {end_date})", 
                "Поставщик", 
                "Сумма заказов"
            )
        except Exception as e:
            logging.error(f"Error showing sales by supplier: {str(e)}")
    
    def show_top_products(self):
        """Отображение топ-продуктов по продажам"""
        try:
            # Получение данных за выбранный период
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # Лимит по количеству товаров
            limit = 10
            
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
            
            result = self.db.fetch_all(query, (start_date, end_date, limit), self)
            
            if not result:
                self.chart_widget.clear_plot()
                return
            
            products = [row[0] for row in result]
            quantities = [row[1] for row in result]
            
            self.chart_widget.plot_bar_chart(
                products, 
                quantities, 
                f"Топ-{limit} продаваемых товаров ({start_date} - {end_date})", 
                "Товар", 
                "Количество"
            )
        except Exception as e:
            logging.error(f"Error showing top products: {str(e)}") 