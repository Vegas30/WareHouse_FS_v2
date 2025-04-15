from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddOrderDialog, ConfirmDialog, ExportDialog

class OrdersTab(QWidget):
    """
    Класс для управления заказами в системе управления складом.
    Наследуется от QWidget для создания пользовательского интерфейса.
    """

    def __init__(self, db):
        """
        Инициализация вкладки заказов.
        
        Args:
            db: Объект базы данных для операций с заказами
        """
        super().__init__()
        # Сохранение объекта базы данных
        self.db = db
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Загрузка списка заказов
        self.load_orders()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создание основного вертикального макета
        main_layout = QVBoxLayout()

        # Создание верхней панели с кнопками управления и фильтрами
        top_panel = QHBoxLayout()

        # Создание кнопок управления
        self.btn_add = QPushButton("Создать заказ")
        self.btn_add.setStyleSheet("background-color: #2e7d32;")  # Зеленый цвет
        self.btn_edit = QPushButton("Редактировать")
        self.btn_cancel = QPushButton("Отменить")
        self.btn_cancel.setStyleSheet("background-color: #d32f2f;")  # Красный цвет

        # Создание фильтра по статусу
        self.status_filter = QComboBox()
        self.status_filter.addItem("Все статусы", None)
        self.status_filter.addItem("В обработке", "в обработке")
        self.status_filter.addItem("Доставлен", "доставлен")
        self.status_filter.addItem("Отменен", "отменен")
        
        # Создание поля поиска
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск заказа...")

        # Добавление растягивающегося элемента
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавление элементов на верхнюю панель
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.btn_cancel)
        top_panel.addWidget(QLabel("Статус:"))
        top_panel.addWidget(self.status_filter)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Создание таблицы для отображения заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Дата", "Поставщик", "Сумма", "Статус", "Обновлено"
        ])
        # Настройка автоматического изменения размера столбцов
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Настройка автоматического изменения размера строк
        self.orders_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создание нижней панели с дополнительными функциями
        bottom_panel = QHBoxLayout()

        # Создание левой части нижней панели - кнопки с иконками
        left_button_panel = QHBoxLayout()

        # Создание кнопки обновления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Создание кнопки деталей заказа
        self.btn_details = QPushButton("Детали заказа")
        self.btn_details.setIcon(QIcon.fromTheme("document-properties"))

        # Добавление кнопок на левую панель
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_details)
        left_button_panel.addStretch()

        # Создание правой части нижней панели - кнопка экспорта
        right_button_panel = QHBoxLayout()
        
        # Создание метки для отображения количества заказов
        self.order_count_label = QLabel("Всего заказов: 0")
        
        # Создание кнопки экспорта
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Добавление элементов на правую панель
        right_button_panel.addWidget(self.order_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Сборка нижней панели из левой и правой частей
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Сборка основного интерфейса
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(bottom_panel)

        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_cancel.clicked.connect(self.cancel_order)
        self.btn_refresh.clicked.connect(self.load_orders)
        self.btn_details.clicked.connect(self.show_order_details)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)

    def load_orders(self):
        """Загрузка заказов из базы данных и отображение в таблице"""
        try:
            # SQL-запрос для получения списка заказов
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, 
                       o.status, o.updated_at
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                ORDER BY o.order_date DESC
            """
            # Получение списка заказов из базы данных
            orders = self.db.fetch_all(query)

            # Установка количества строк в таблице
            self.orders_table.setRowCount(len(orders))

            # Заполнение таблицы данными
            for row_idx, order in enumerate(orders):
                for col_idx, data in enumerate(order):
                    # Создание элемента таблицы
                    item = QTableWidgetItem(str(data))
                    # Запрет редактирования ячеек
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Цветовое кодирование столбца статуса
                    if col_idx == 4:  # Столбец статуса
                        if data == "доставлен":
                            item.setForeground(Qt.GlobalColor.darkGreen)
                        elif data == "отменен":
                            item.setForeground(Qt.GlobalColor.red)
                        elif data == "в обработке":
                            item.setForeground(Qt.GlobalColor.blue)
                    
                    # Установка элемента в таблицу
                    self.orders_table.setItem(row_idx, col_idx, item)
            
            # Обновление счетчика заказов
            self.order_count_label.setText(f"Всего заказов: {len(orders)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки заказов: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о заказах")

    def handle_search(self):
        """Обработка изменений в поиске и фильтрах"""
        self.apply_filters()

    def apply_filters(self):
        """Применение фильтров к таблице заказов"""
        try:
            # Получение текста поиска
            search_text = self.search.text()
            # Получение выбранного статуса
            status_filter = self.status_filter.currentData()
            
            # Базовый SQL-запрос
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, 
                       o.status, o.updated_at
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                WHERE 1=1
            """
            params = []
            
            # Добавление фильтра по статусу
            if status_filter:
                query += " AND o.status = %s"
                params.append(status_filter)
            
            # Добавление фильтра поиска
            if search_text:
                query += """ AND (
                    o.order_id::text LIKE %s
                    OR s.supplier_name ILIKE %s
                )"""
                search_param = f"%{search_text}%"
                params.extend([search_param, search_param])
            
            # Добавление сортировки
            query += " ORDER BY o.order_date DESC"
            
            # Выполнение запроса
            orders = self.db.fetch_all(query, tuple(params))
            
            # Обновление таблицы
            self.orders_table.setRowCount(len(orders))
            
            # Заполнение таблицы отфильтрованными данными
            for row_idx, order in enumerate(orders):
                for col_idx, data in enumerate(order):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Цветовое кодирование столбца статуса
                    if col_idx == 4:  # Столбец статуса
                        if data == "доставлен":
                            item.setForeground(Qt.GlobalColor.darkGreen)
                        elif data == "отменен":
                            item.setForeground(Qt.GlobalColor.red)
                        elif data == "в обработке":
                            item.setForeground(Qt.GlobalColor.blue)
                    
                    self.orders_table.setItem(row_idx, col_idx, item)
            
            # Обновление счетчика заказов
            self.order_count_label.setText(f"Найдено заказов: {len(orders)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка фильтрации заказов: {str(e)}")

    def add_order(self):
        """Отображение диалога создания нового заказа"""
        # Создание диалога добавления заказа
        dialog = AddOrderDialog(self, self.db)
        if dialog.exec():
            # Получение данных заказа из диалога
            order_data = dialog.get_order_data()
            try:
                # SQL-запрос для добавления заказа
                query = """
                    INSERT INTO orders (order_date, supplier_id, total_amount, status)
                    VALUES (%s, %s, %s, %s)
                """
                # Параметры запроса
                params = (
                    order_data["date"],
                    order_data["supplier_id"],
                    order_data["amount"],
                    order_data["status"]
                )
                # Выполнение запроса
                success = self.db.execute_query(query, params)
                if success:
                    # Обновление списка заказов
                    self.load_orders()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Заказ успешно создан")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось создать заказ")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка создания заказа: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")

    def edit_order(self):
        """Редактирование выбранного заказа"""
        # Получение выбранных строк
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если заказ не выбран
            QMessageBox.warning(self, "Внимание", "Выберите заказ для редактирования")
            return
            
        # Получение номера строки и ID заказа
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        # Получение статуса заказа
        status = self.orders_table.item(row, 4).text()
        
        # Проверка возможности редактирования
        if status == "доставлен" or status == "отменен":
            QMessageBox.warning(self, "Внимание", "Нельзя редактировать завершенный или отмененный заказ")
            return
            
        try:
            # Получение данных заказа
            query = """
                SELECT order_date, supplier_id, total_amount, status 
                FROM orders 
                WHERE order_id = %s
            """
            order_data = self.db.fetch_one(query, (order_id,))
            
            if order_data:
                # Создание диалога редактирования
                dialog = AddOrderDialog(self, self.db)
                dialog.setWindowTitle("Редактировать заказ")
                
                # Установка текущих данных в поля диалога
                dialog.date_input.setDate(Qt.QDate.fromString(str(order_data[0]), "yyyy-MM-dd"))
                
                # Поиск индекса поставщика
                supplier_idx = -1
                for i in range(dialog.supplier_input.count()):
                    if dialog.supplier_input.itemData(i) == order_data[1]:
                        supplier_idx = i
                        break
                if supplier_idx >= 0:
                    dialog.supplier_input.setCurrentIndex(supplier_idx)
                
                # Установка суммы
                dialog.amount_input.setValue(float(order_data[2]))
                
                # Поиск индекса статуса
                status_idx = dialog.status_input.findText(order_data[3])
                if status_idx >= 0:
                    dialog.status_input.setCurrentIndex(status_idx)
                
                if dialog.exec():
                    # Получение обновленных данных
                    updated_data = dialog.get_order_data()
                    # SQL-запрос для обновления заказа
                    update_query = """
                        UPDATE orders 
                        SET order_date = %s, 
                            supplier_id = %s, 
                            total_amount = %s, 
                            status = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE order_id = %s
                    """
                    # Параметры запроса
                    update_params = (
                        updated_data["date"],
                        updated_data["supplier_id"],
                        updated_data["amount"],
                        updated_data["status"],
                        order_id
                    )
                    # Выполнение запроса
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        # Обновление списка заказов
                        self.load_orders()
                        # Отображение сообщения об успехе
                        QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
                    else:
                        # Отображение сообщения об ошибке
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить заказ")
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка редактирования заказа: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать заказ: {str(e)}")

    def cancel_order(self):
        """Отмена выбранного заказа"""
        # Получение выбранных строк
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если заказ не выбран
            QMessageBox.warning(self, "Внимание", "Выберите заказ для отмены")
            return
            
        # Получение номера строки и ID заказа
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        # Получение статуса заказа
        status = self.orders_table.item(row, 4).text()
        
        # Проверка возможности отмены
        if status == "доставлен" or status == "отменен":
            QMessageBox.warning(self, "Внимание", "Нельзя отменить завершенный или уже отмененный заказ")
            return
            
        # Создание диалога подтверждения
        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение отмены заказа",
            f"Вы действительно хотите отменить заказ #{order_id}?"
        )
        
        if confirm_dialog.exec():
            try:
                # SQL-запрос для отмены заказа
                query = """
                    UPDATE orders 
                    SET status = 'отменен', 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE order_id = %s
                """
                # Выполнение запроса
                success = self.db.execute_query(query, (order_id,))
                if success:
                    # Обновление списка заказов
                    self.load_orders()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Заказ успешно отменен")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось отменить заказ")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка отмены заказа: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось отменить заказ: {str(e)}")

    def show_order_details(self):
        """Отображение деталей выбранного заказа"""
        # Получение выбранных строк
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если заказ не выбран
            QMessageBox.warning(self, "Внимание", "Выберите заказ для просмотра деталей")
            return
            
        # Получение номера строки и ID заказа
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        
        try:
            # Получение товаров в заказе
            query = """
                SELECT p.product_name, oi.quantity, oi.unit_price, oi.total_price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            """
            items = self.db.fetch_all(query, (order_id,))
            
            # Форматирование текста деталей
            details_text = f"Детали заказа #{order_id}:\n\n"
            
            if items:
                details_text += "Товары в заказе:\n"
                details_text += "--------------------------------\n"
                details_text += "Товар | Кол-во | Цена | Сумма\n"
                details_text += "--------------------------------\n"
                
                # Добавление информации о каждом товаре
                for item in items:
                    details_text += f"{item[0]} | {item[1]} | {item[2]}₽ | {item[3]}₽\n"
                
                details_text += "--------------------------------\n"
                details_text += f"Общая сумма: {self.orders_table.item(row, 3).text()}₽"
            else:
                details_text += "В этом заказе нет товаров"
            
            # Отображение деталей заказа
            QMessageBox.information(self, "Детали заказа", details_text)
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка отображения деталей заказа: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить детали заказа: {str(e)}")

    def export_data(self):
        """Экспорт данных о заказах"""
        # Создание диалога экспорта
        dialog = ExportDialog(self, "Экспорт заказов")
        if dialog.exec():
            # Получение данных для экспорта
            export_data = dialog.get_export_data()
            file_path = export_data["file_path"]
            
            if not file_path:
                # Отображение предупреждения, если путь не выбран
                QMessageBox.warning(self, "Внимание", "Выберите путь для сохранения файла")
                return
            
            # Здесь будет реализация экспорта
            # Это просто заглушка
            QMessageBox.information(self, "Экспорт", f"Данные успешно экспортированы в {file_path}") 