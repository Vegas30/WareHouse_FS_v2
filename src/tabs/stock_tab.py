from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QSpinBox, QDateEdit, QComboBox, QFormLayout,
    QDialog, QDialogButtonBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
import logging
from data_export import DataExporter
from dialogs import ExportDialog
from validators import Validator
from visualization import InventoryAnalysisDialog

class StockTab(QWidget):
    """
    Класс для управления запасами в системе управления складом.
    Наследуется от QWidget для создания пользовательского интерфейса.
    """

    def __init__(self, db):
        """
        Инициализация вкладки запасов.
        
        Args:
            db: Объект базы данных для операций с запасами
        """
        super().__init__()
        # Сохранение объекта базы данных
        self.db = db
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Загрузка списка запасов
        self.load_stock()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создание основного вертикального макета
        main_layout = QVBoxLayout()

        # Создание верхней панели с кнопками управления и фильтрами
        top_panel = QHBoxLayout()

        # Создание кнопок управления
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Обновить запас")
        self.btn_move = QPushButton("Переместить")

        # Создание фильтра по складу
        self.warehouse_filter = QComboBox()
        self.warehouse_filter.setMinimumWidth(200)
        self.warehouse_filter.addItem("Все склады", None)
        # Загрузка списка складов
        self.load_warehouses()
        
        # Создание фильтра по категории
        self.category_filter = QComboBox()
        self.category_filter.setMinimumWidth(150)
        self.category_filter.addItem("Все категории", None)
        # Загрузка списка категорий
        self.load_categories()
        
        # Создание поля поиска
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск товара...")

        # Добавление растягивающегося элемента
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавление элементов на верхнюю панель
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_update)
        top_panel.addWidget(self.btn_move)
        top_panel.addWidget(QLabel("Склад:"))
        top_panel.addWidget(self.warehouse_filter)
        top_panel.addWidget(QLabel("Категория:"))
        top_panel.addWidget(self.category_filter)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Создание таблицы для отображения запасов
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(7)
        self.stock_table.setHorizontalHeaderLabels([
            "ID", "Товар", "Склад", "Количество", 
            "Последнее пополнение", "Категория", "Цена за ед."
        ])
        # Настройка автоматического изменения размера столбцов
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Настройка автоматического изменения размера строк
        self.stock_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создание нижней панели с дополнительными функциями
        bottom_panel = QHBoxLayout()

        # Создание левой части нижней панели - кнопки с иконками
        left_button_panel = QHBoxLayout()

        # Создание кнопки обновления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Создание кнопки отчета
        self.btn_report = QPushButton("Отчет")
        self.btn_report.setIcon(QIcon.fromTheme("x-office-document"))
        
        # Создание кнопки анализа
        self.btn_analysis = QPushButton("Анализ запасов")
        self.btn_analysis.setIcon(QIcon.fromTheme("accessories-calculator"))

        # Добавление кнопок на левую панель
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_report)
        left_button_panel.addWidget(self.btn_analysis)
        left_button_panel.addStretch()

        # Создание правой части нижней панели - кнопки экспорта и предупреждение о низком запасе
        right_button_panel = QHBoxLayout()
        
        # Создание метки для предупреждения о низком запасе
        self.low_stock_label = QLabel("Товары с низким запасом: 0")
        self.low_stock_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
        
        # Создание кнопок экспорта
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # self.btn_export_csv = QPushButton("Экспорт в CSV")
        # self.btn_export_csv.setIcon(QIcon.fromTheme("document-save"))
        
        # self.btn_export_excel = QPushButton("Экспорт в Excel")
        # self.btn_export_excel.setIcon(QIcon.fromTheme("x-office-spreadsheet"))

        # Добавление элементов на правую панель
        right_button_panel.addWidget(self.low_stock_label)
        right_button_panel.addStretch()
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)
        # right_button_panel.addWidget(self.btn_export_csv)
        # right_button_panel.addWidget(self.btn_export_excel)

        # Сборка нижней панели из левой и правой частей
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Сборка основного интерфейса
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.stock_table)
        main_layout.addLayout(bottom_panel)

        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.add_stock)
        self.btn_update.clicked.connect(self.update_stock)
        self.btn_move.clicked.connect(self.move_stock)
        self.btn_refresh.clicked.connect(self.load_stock)
        self.btn_report.clicked.connect(self.generate_report)
        self.btn_export.clicked.connect(self.export_data)
        # self.btn_export_csv.clicked.connect(self.export_to_csv)
        # self.btn_export_excel.clicked.connect(self.export_to_excel)
        self.btn_analysis.clicked.connect(self.show_analysis)
        self.search.textChanged.connect(self.handle_search)
        self.warehouse_filter.currentIndexChanged.connect(self.load_stock)
        self.category_filter.currentIndexChanged.connect(self.load_stock)

    def load_warehouses(self):
        """Загрузка списка складов для фильтра"""
        try:
            # SQL-запрос для получения списка складов
            query = "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name"
            # Получение списка складов из базы данных
            warehouses = self.db.fetch_all(query, parent_widget=self)
            
            # Добавление складов в фильтр
            for warehouse_id, warehouse_name in warehouses:
                self.warehouse_filter.addItem(warehouse_name, warehouse_id)
                
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки складов: {str(e)}")
    
    def load_categories(self):
        """Загрузка списка категорий для фильтра"""
        try:
            # SQL-запрос для получения списка категорий
            query = "SELECT DISTINCT category FROM products ORDER BY category"
            # Получение списка категорий из базы данных
            categories = self.db.fetch_all(query, parent_widget=self)
            
            # Добавление категорий в фильтр
            for category in categories:
                self.category_filter.addItem(category[0], category[0])
                
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки категорий: {str(e)}")

    def load_stock(self):
        """Загрузка данных о запасах из базы данных и отображение в таблице"""
        try:
            # Получение выбранных фильтров
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Базовый SQL-запрос
            query = """
                SELECT s.stock_id, p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Добавление фильтра по складу
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Добавление фильтра по категории
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Добавление фильтра поиска
            if search_text:
                # Очистка ввода для поиска
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Добавление сортировки
            query += " ORDER BY p.product_name"
            
            # Выполнение запроса
            stock_data = self.db.fetch_all(query, params, parent_widget=self)

            # Установка количества строк в таблице
            self.stock_table.setRowCount(len(stock_data))
            
            # Счетчик товаров с низким запасом
            low_stock_count = 0
            # Порог для определения низкого запаса
            low_stock_threshold = 10
            
            # Заполнение таблицы данными
            for row_idx, stock_item in enumerate(stock_data):
                for col_idx, data in enumerate(stock_item):
                    # Создание элемента таблицы
                    item = QTableWidgetItem(str(data))
                    # Запрет редактирования ячеек
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Подсветка товаров с низким запасом
                    if col_idx == 3 and int(data) < low_stock_threshold:
                        item.setForeground(Qt.GlobalColor.red)
                        low_stock_count += 1
                        
                    # Установка элемента в таблицу
                    self.stock_table.setItem(row_idx, col_idx, item)
            
            # Обновление метки с количеством товаров с низким запасом
            self.low_stock_label.setText(f"Товары с низким запасом: {low_stock_count}")
            
            # Изменение цвета метки в зависимости от наличия товаров с низким запасом
            if low_stock_count > 0:
                self.low_stock_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
            else:
                self.low_stock_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки запасов: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о запасах")

    def handle_search(self):
        """Обработка поиска запасов"""
        self.load_stock()

    def check_low_stock_alert(self):
        """Проверка наличия товаров с критически низким запасом и отображение предупреждения"""
        try:
            # Определение критического порога
            critical_threshold = 5
            
            # SQL-запрос для поиска товаров с критически низким запасом
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE s.quantity < %s
                ORDER BY s.quantity
            """
            
            # Получение списка товаров с критически низким запасом
            critical_items = self.db.fetch_all(query, (critical_threshold,), parent_widget=self)
            
            if critical_items:
                # Формирование сообщения с предупреждением
                alert_message = "Внимание! Критически низкий уровень запасов:\n\n"
                
                # Добавление информации о каждом товаре
                for item in critical_items:
                    product_name, warehouse_name, quantity = item
                    alert_message += f"• {product_name} ({warehouse_name}): {quantity} шт.\n"
                
                # Отображение предупреждения
                QMessageBox.warning(self, "Низкий уровень запасов", alert_message)
        
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка проверки низкого запаса: {str(e)}")

    def add_stock(self):
        """Открытие диалога добавления нового запаса"""
        # Создание диалога добавления запаса
        dialog = AddStockDialog(self, self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Обновление списка запасов после добавления
            self.load_stock()

    def update_stock(self):
        """Обновление количества запаса для выбранного товара"""
        # Получение выбранной строки
        selected_row = self.stock_table.currentRow()
        
        if selected_row >= 0:
            # Получение данных о выбранном запасе
            stock_id = self.stock_table.item(selected_row, 0).text()
            product_name = self.stock_table.item(selected_row, 1).text()
            current_quantity = int(self.stock_table.item(selected_row, 3).text())
            
            # Создание диалога обновления запаса
            dialog = UpdateStockDialog(self, product_name, current_quantity)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Получение нового количества
                new_quantity = dialog.get_quantity()
                
                try:
                    # SQL-запрос для обновления количества запаса
                    query = """
                        UPDATE stock 
                        SET quantity = %s, last_restocked = CURRENT_DATE
                        WHERE stock_id = %s
                    """
                    
                    # Выполнение запроса
                    success = self.db.execute_query(query, (new_quantity, stock_id), parent_widget=self)
                    
                    if success:
                        # Обновление списка запасов
                        self.load_stock()
                        # Отображение сообщения об успехе
                        QMessageBox.information(self, "Успех", "Количество товара обновлено")
                
                except Exception as e:
                    # Логирование ошибки
                    logging.error(f"Ошибка обновления запаса: {str(e)}")
                    # Отображение сообщения об ошибке
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить количество товара")
        else:
            # Отображение предупреждения, если товар не выбран
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для обновления")

    def move_stock(self):
        """Перемещение запаса с одного склада на другой"""
        # Получение выбранной строки
        selected_row = self.stock_table.currentRow()
        
        if selected_row >= 0:
            # Получение данных о выбранном запасе
            stock_id = self.stock_table.item(selected_row, 0).text()
            product_name = self.stock_table.item(selected_row, 1).text()
            source_warehouse = self.stock_table.item(selected_row, 2).text()
            current_quantity = int(self.stock_table.item(selected_row, 3).text())
            
            # Создание диалога перемещения запаса
            dialog = MoveStockDialog(self, self.db, product_name, source_warehouse, current_quantity)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Получение данных для перемещения
                target_warehouse_id, quantity_to_move = dialog.get_move_data()
                
                # Проверка возможности перемещения
                if quantity_to_move > current_quantity:
                    QMessageBox.warning(self, "Предупреждение", "Нельзя переместить больше товара, чем имеется на складе")
                    return
                
                try:
                    # Получение ID товара
                    query = "SELECT product_id FROM stock WHERE stock_id = %s"
                    product_id = self.db.fetch_one(query, (stock_id,), parent_widget=self)[0]
                    
                    # Обновление количества на исходном складе
                    query = """
                        UPDATE stock 
                        SET quantity = quantity - %s
                        WHERE stock_id = %s
                    """
                    self.db.execute_query(query, (quantity_to_move, stock_id), parent_widget=self)
                    
                    # Проверка наличия товара на целевом складе
                    query = """
                        SELECT stock_id, quantity 
                        FROM stock 
                        WHERE product_id = %s AND warehouse_id = %s
                    """
                    target_stock = self.db.fetch_one(query, (product_id, target_warehouse_id), parent_widget=self)
                    
                    if target_stock:
                        # Обновление количества на целевом складе
                        target_stock_id, target_quantity = target_stock
                        query = """
                            UPDATE stock 
                            SET quantity = quantity + %s
                            WHERE stock_id = %s
                        """
                        self.db.execute_query(query, (quantity_to_move, target_stock_id), parent_widget=self)
                    else:
                        # Создание новой записи на целевом складе
                        query = """
                            INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
                            VALUES (%s, %s, %s, CURRENT_DATE)
                        """
                        self.db.execute_query(query, (product_id, target_warehouse_id, quantity_to_move), parent_widget=self)
                    
                    # Обновление списка запасов
                    self.load_stock()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", f"Товар успешно перемещен ({quantity_to_move} шт.)")
                
                except Exception as e:
                    # Логирование ошибки
                    logging.error(f"Ошибка перемещения запаса: {str(e)}")
                    # Отображение сообщения об ошибке
                    QMessageBox.critical(self, "Ошибка", "Не удалось переместить товар")
        else:
            # Отображение предупреждения, если товар не выбран
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для перемещения")
    
    def generate_report(self):
        """Генерация отчета по запасам"""
        try:
            # Получение выбранных фильтров
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            
            # Заголовок и начало сообщения отчета
            title = "Отчет по запасам"
            message = "Сводная информация по запасам:\n\n"
            
            # SQL-запрос для получения общей стоимости запасов
            value_query = """
                SELECT SUM(p.unit_price * s.quantity) as total_value
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1
            """
            
            # SQL-запрос для получения запасов по категориям
            category_query = """
                SELECT p.category, SUM(s.quantity) as total_quantity
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1
            """
            
            # SQL-запрос для получения количества товаров с низким запасом
            low_stock_query = """
                SELECT COUNT(*) 
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE s.quantity < 10
            """
            
            params = []
            
            # Добавление фильтра по складу
            if selected_warehouse:
                value_query += " AND s.warehouse_id = %s"
                category_query += " AND s.warehouse_id = %s"
                low_stock_query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Добавление фильтра по категории
            if selected_category:
                value_query += " AND p.category = %s"
                category_query += " AND p.category = %s"
                low_stock_query += " AND p.category = %s"
                params.append(selected_category)
            
            # Добавление группировки и сортировки для запроса по категориям
            category_query += " GROUP BY p.category ORDER BY total_quantity DESC"
            
            # Получение общей стоимости запасов
            total_value = self.db.fetch_one(value_query, params, parent_widget=self)
            if total_value and total_value[0]:
                message += f"Общая стоимость запасов: {total_value[0]:.2f} руб.\n\n"
            
            # Получение запасов по категориям
            categories = self.db.fetch_all(category_query, params, parent_widget=self)
            if categories:
                message += "Распределение по категориям:\n"
                for category, quantity in categories:
                    message += f"• {category}: {quantity} шт.\n"
                message += "\n"
            
            # Получение количества товаров с низким запасом
            low_stock_count = self.db.fetch_one(low_stock_query, params, parent_widget=self)
            if low_stock_count:
                message += f"Товаров с низким запасом: {low_stock_count[0]}\n"
            
            # Отображение отчета
            QMessageBox.information(self, title, message)
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка генерации отчета: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось сформировать отчет")

    def export_data(self):
        """Экспорт данных о товарах"""
        # Создание диалога экспорта
        dialog = ExportDialog(self, "Экспорт запасов")
        if dialog.exec():
            # Получение данных для экспорта
            export_data = dialog.get_export_data()
            file_path = export_data["file_path"]
            export_format = export_data["format"]
            
            if not file_path:
                # Отображение предупреждения, если путь не выбран
                QMessageBox.warning(self, "Внимание", "Выберите путь для сохранения файла")
                return

            try:
                # Получение выбранных фильтров
                selected_warehouse = self.warehouse_filter.currentData()
                selected_category = self.category_filter.currentData()
                search_text = self.search.text()

                # SQL-запрос для получения данных о товарах
                query = """
                    SELECT p.product_name, w.warehouse_name, s.quantity, 
                        s.last_restocked, p.category, p.unit_price
                    FROM stock s
                    JOIN products p ON s.product_id = p.product_id
                    JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                    WHERE 1=1
                """

                params = []

                # Добавление фильтра по складу
                if selected_warehouse:
                    query += " AND s.warehouse_id = %s"
                    params.append(selected_warehouse)
                
                # Добавление фильтра по категории
                if selected_category:
                    query += " AND p.category = %s"
                    params.append(selected_category)
                
                # Добавление фильтра поиска
                if search_text:
                    # Очистка ввода для поиска
                    search_text = Validator.sanitize_input(search_text)
                    query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                    params.extend([f"%{search_text}%", f"%{search_text}%"])
                
                # Добавление сортировки
                query += " ORDER BY p.product_name"
                
                # Заголовки для экспорта
                headers = ["Товар", "Склад", "Количество", "Последнее пополнение", "Категория", "Цена за ед."]
                
                # Создание объекта для экспорта
                exporter = DataExporter(self)
                
                # Экспорт в зависимости от выбранного формата
                if "Excel" in export_format:
                    success = exporter.export_to_excel(
                        query=query,
                        params=params,
                        filename=file_path,
                        headers=headers,
                        sheet_name="Товары"
                    )
                elif "CSV" in export_format:
                    success = exporter.export_to_csv(
                        query=query,
                        params=params,
                        filename=file_path,
                        headers=headers
                    )
                elif "PDF" in export_format:
                    success = exporter.export_to_pdf(
                        query=query,
                        params=params,
                        filename=file_path,
                        headers=headers,
                        title="Отчет по товарам"
                    )
                else:
                    # Отображение предупреждения о неподдерживаемом формате
                    QMessageBox.warning(self, "Экспорт", "Формат не поддерживается")
                    return
                
                if not success:
                    # Отображение сообщения об ошибке
                    QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать данные")
                    
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка экспорта товаров: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте данных: {str(e)}")


    def export_to_csv(self):
        """Экспорт данных о запасах в CSV файл"""
        try:
            # Получение выбранных фильтров
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Базовый SQL-запрос
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Добавление фильтра по складу
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Добавление фильтра по категории
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Добавление фильтра поиска
            if search_text:
                # Очистка ввода для поиска
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Добавление сортировки
            query += " ORDER BY p.product_name"
            
            # Определение заголовков
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение", "Категория", "Цена за ед."]
            
            # Экспорт данных
            exporter = DataExporter(self)
            exporter.export_to_csv(query, params, headers=headers)
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка экспорта в CSV: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать данные в CSV")
    
    def export_to_excel(self):
        """Экспорт данных о запасах в Excel файл"""
        try:
            # Получение выбранных фильтров
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Базовый SQL-запрос
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Добавление фильтра по складу
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Добавление фильтра по категории
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Добавление фильтра поиска
            if search_text:
                # Очистка ввода для поиска
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Добавление сортировки
            query += " ORDER BY p.product_name"
            
            # Определение заголовков
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение", "Категория", "Цена за ед."]
            
            # Экспорт данных
            exporter = DataExporter(self)
            exporter.export_to_excel(query, params, headers=headers, sheet_name="Запасы")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка экспорта в Excel: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать данные в Excel")
    
    def show_analysis(self):
        """Отображение диалога анализа запасов с визуализациями"""
        try:
            # Создание и отображение диалога анализа
            dialog = InventoryAnalysisDialog(self)
            dialog.exec()
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка отображения анализа: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть анализ запасов")

    def showEvent(self, event):
        """Вызывается при отображении вкладки"""
        super().showEvent(event)
        # Проверка низкого уровня запасов при показе вкладки
        self.check_low_stock_alert()


class AddStockDialog(QDialog):
    """Диалог для добавления нового запаса"""
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Добавить запас")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Инициализация списков товаров и складов
        self.products = []
        self.warehouses = []
        # Загрузка данных
        self.load_data()
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    def load_data(self):
        """Загрузка данных о товарах и складах"""
        if not self.db:
            return
            
        try:
            # Загрузка списка товаров
            product_query = "SELECT product_id, product_name FROM products ORDER BY product_name"
            self.products = self.db.fetch_all(product_query)
            
            # Загрузка списка складов
            warehouse_query = "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name"
            self.warehouses = self.db.fetch_all(warehouse_query)
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки данных для диалога запасов: {str(e)}")
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса диалога"""
        # Создание основного макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Добавить запас товара")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Создание формы
        form = QFormLayout()
        
        # Создание выпадающего списка товаров
        self.product_combo = QComboBox()
        for product_id, product_name in self.products:
            self.product_combo.addItem(product_name, product_id)
        form.addRow("Товар:", self.product_combo)
        
        # Создание выпадающего списка складов
        self.warehouse_combo = QComboBox()
        for warehouse_id, warehouse_name in self.warehouses:
            self.warehouse_combo.addItem(warehouse_name, warehouse_id)
        form.addRow("Склад:", self.warehouse_combo)
        
        # Создание поля для ввода количества
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 100000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Количество:", self.quantity_spin)
        
        # Создание поля для выбора даты
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form.addRow("Дата поступления:", self.date_edit)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление кнопок в основной макет
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def accept(self):
        """Обработка нажатия кнопки OK"""
        try:
            # Получение выбранных данных
            product_id = self.product_combo.currentData()
            warehouse_id = self.warehouse_combo.currentData()
            quantity = self.quantity_spin.value()
            restock_date = self.date_edit.date().toString("yyyy-MM-dd")
            
            # Проверка наличия товара на складе
            check_query = "SELECT stock_id FROM stock WHERE product_id = %s AND warehouse_id = %s"
            existing_stock = self.db.fetch_one(check_query, (product_id, warehouse_id))
            
            if existing_stock:
                # Обновление существующего запаса
                update_query = """
                    UPDATE stock 
                    SET quantity = quantity + %s,
                        last_restocked = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE product_id = %s AND warehouse_id = %s
                """
                success = self.db.execute_query(update_query, (quantity, restock_date, product_id, warehouse_id))
            else:
                # Добавление нового запаса
                insert_query = """
                    INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
                    VALUES (%s, %s, %s, %s)
                """
                success = self.db.execute_query(insert_query, (product_id, warehouse_id, quantity, restock_date))
                
            if success:
                super().accept()
            else:
                # Отображение сообщения об ошибке
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить запас")
                
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка добавления запаса: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запас: {str(e)}")


class UpdateStockDialog(QDialog):
    """Диалог для обновления количества запаса"""
    def __init__(self, parent=None, product_name="", current_quantity=0):
        super().__init__(parent)
        # Установка заголовка окна
        self.setWindowTitle("Обновить запас")
        # Сохранение данных о товаре
        self.product_name = product_name
        self.current_quantity = current_quantity
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса диалога"""
        # Создание основного макета
        layout = QVBoxLayout()
        
        # Создание заголовка с названием товара
        title = QLabel(f"Обновить запас: {self.product_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Создание формы
        form = QFormLayout()
        
        # Создание метки с текущим количеством
        current_label = QLabel(str(self.current_quantity))
        current_label.setStyleSheet("font-weight: bold;")
        form.addRow("Текущее количество:", current_label)
        
        # Создание поля для ввода нового количества
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 100000)
        self.quantity_spin.setValue(self.current_quantity)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Новое количество:", self.quantity_spin)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление кнопок в основной макет
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def get_quantity(self):
        """Получение нового количества"""
        return self.quantity_spin.value()


class MoveStockDialog(QDialog):
    """Диалог для перемещения запаса между складами"""
    def __init__(self, parent=None, db=None, product_name="", source_warehouse="", current_quantity=0):
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Переместить товар")
        # Сохранение данных о товаре
        self.product_name = product_name
        self.source_warehouse = source_warehouse
        self.current_quantity = current_quantity
        # Инициализация списка складов
        self.warehouses = []
        # Загрузка списка складов
        self.load_warehouses()
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    def load_warehouses(self):
        """Загрузка списка складов"""
        if not self.db:
            return
            
        try:
            # Загрузка списка складов, исключая исходный склад
            query = """
                SELECT warehouse_id, warehouse_name 
                FROM warehouses 
                WHERE warehouse_name != %s
                ORDER BY warehouse_name
            """
            self.warehouses = self.db.fetch_all(query, (self.source_warehouse,))
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки складов для диалога перемещения: {str(e)}")
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса диалога"""
        # Создание основного макета
        layout = QVBoxLayout()
        
        # Создание заголовка с названием товара
        title = QLabel(f"Переместить товар: {self.product_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Создание формы
        form = QFormLayout()
        
        # Создание метки с исходным складом
        source_label = QLabel(self.source_warehouse)
        source_label.setStyleSheet("font-weight: bold;")
        form.addRow("Исходный склад:", source_label)
        
        # Создание выпадающего списка целевых складов
        self.target_combo = QComboBox()
        for warehouse_id, warehouse_name in self.warehouses:
            self.target_combo.addItem(warehouse_name, warehouse_id)
        form.addRow("Целевой склад:", self.target_combo)
        
        # Создание метки с доступным количеством
        available_label = QLabel(str(self.current_quantity))
        available_label.setStyleSheet("font-weight: bold;")
        form.addRow("Доступное количество:", available_label)
        
        # Создание поля для ввода количества для перемещения
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, self.current_quantity)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Количество для перемещения:", self.quantity_spin)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление кнопок в основной макет
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def get_move_data(self):
        """Получение данных для перемещения"""
        return {
            "target_warehouse_id": self.target_combo.currentData(),
            "target_warehouse_name": self.target_combo.currentText(),
            "quantity": self.quantity_spin.value()
        } 