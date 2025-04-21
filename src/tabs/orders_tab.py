from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QComboBox, QSpacerItem, QSizePolicy, QDialog, QSplitter, QMenu, QInputDialog, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddOrderDialog, ConfirmDialog, ExportDialog, CreatePurchaseOrderDialog
import datetime

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

        # Splitter for Orders and Order Items tables
        splitter = QSplitter(Qt.Orientation.Vertical)

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

        self.orders_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.orders_table.customContextMenuRequested.connect(self.show_order_context_menu)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Select whole rows
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Make read-only
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        splitter.addWidget(self.orders_table)
        # Order Items Table
        self.order_items_table = QTableWidget()
        # Columns for order_items table: order_item_id, product_id, quantity, unit_price, total_price
        self.order_items_table.setColumnCount(5)
        self.order_items_table.setHorizontalHeaderLabels(
            ["ID Позиции", "Товар", "Кол-во", "Цена за ед.", "Итого"]
        )
        self.order_items_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.order_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        splitter.addWidget(self.order_items_table)

        # Set initial sizes for splitter panes (optional)
        splitter.setSizes([400, 200])

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
        main_layout.addWidget(splitter)
        main_layout.addLayout(bottom_panel)


        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.create_purchase_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_cancel.clicked.connect(self.cancel_order)
        self.btn_refresh.clicked.connect(self.load_orders)
        self.btn_details.clicked.connect(self.show_order_details)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)
        # Добавление сигнала для загрузки позиций заказа при выборе
        self.orders_table.itemSelectionChanged.connect(self.load_order_items)

    def load_orders(self):
        """Загрузка заказов из базы данных и отображение в таблице"""
        try:
            # Очистка таблицы позиций при перезагрузке заказов
            self.order_items_table.setRowCount(0)
            
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
                    
                    # Форматирование денежных сумм
                    if col_idx == 3:  # Столбец с суммой
                        item = QTableWidgetItem(f"{data:.2f}")
                    
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
            # Очистка таблицы позиций при фильтрации заказов
            self.order_items_table.setRowCount(0)
        
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
                    
                    # Форматирование денежных сумм
                    if col_idx == 3:  # Столбец с суммой
                        item = QTableWidgetItem(f"{data:.2f}")
                    
                    self.orders_table.setItem(row_idx, col_idx, item)
            
            # Обновление счетчика заказов
            self.order_count_label.setText(f"Найдено заказов: {len(orders)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка фильтрации заказов: {str(e)}")
    
    def load_order_items(self):
        """Загружает позиции для выбранного заказа в нижнюю таблицу."""
        try:
            # Получение выбранных строк
            selected_rows = self.orders_table.selectionModel().selectedRows()
            if not selected_rows:
                # Очистка таблицы товаров, если заказ не выбран
                self.order_items_table.setRowCount(0)
                return

            # Получение индекса выбранной строки и ID заказа
            selected_row_index = selected_rows[0].row()
            order_id_item = self.orders_table.item(selected_row_index, 0)

            if not order_id_item:
                self.order_items_table.setRowCount(0)
                return

            order_id = int(order_id_item.text())

            # Запрос позиций заказа с названиями товаров
            query = """
                SELECT oi.order_item_id, p.product_name, oi.quantity, oi.unit_price, oi.total_price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
            """
            items = self.db.fetch_all(query, (order_id,))

            # Обновление заголовков таблицы позиций
            self.order_items_table.setHorizontalHeaderLabels([
                "ID", "Товар", "Количество", "Цена за ед.", "Итого"
            ])

            # Заполнение таблицы позиций заказа
            self.order_items_table.setRowCount(len(items))
            for row_idx, item_data in enumerate(items):
                for col_idx, data in enumerate(item_data):
                    # Создание элемента таблицы
                    if col_idx in [3, 4]:  # Форматирование денежных значений
                        table_item = QTableWidgetItem(f"{data:.2f}")
                    else:
                        table_item = QTableWidgetItem(str(data))
                        
                    # Запрет редактирования ячеек
                    table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.order_items_table.setItem(row_idx, col_idx, table_item)

        except Exception as e:
            # Логирование ошибки и отображение сообщения
            logging.error(f"Ошибка загрузки позиций заказа {order_id}: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить позиции заказа {order_id}")
            self.order_items_table.setRowCount(0)

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
           # Получаем текущие данные заказа
           query_order = """
               SELECT o.supplier_id, o.total_amount, o.status
               FROM orders o
               WHERE o.order_id = %s
           """
           self.db.cursor.execute(query_order, (order_id,))
           order_data = self.db.cursor.fetchone()
           
           if not order_data:
               QMessageBox.critical(self, "Ошибка", f"Информация о заказе ID {order_id} не найдена.")
               return
                   
           # Получаем позиции заказа
           query_items = """
               SELECT oi.order_item_id, oi.product_id, p.product_name, oi.quantity, oi.unit_price, oi.total_price
               FROM order_items oi
               JOIN products p ON oi.product_id = p.product_id
               WHERE oi.order_id = %s
               ORDER BY oi.order_item_id
           """
           self.db.cursor.execute(query_items, (order_id,))
           order_items = self.db.cursor.fetchall()
           
           # Создаем диалог редактирования заказа
           edit_dialog = AddOrderDialog(self, self.db)
           edit_dialog.setWindowTitle("Редактировать заказ")
           
           # Заполняем диалог текущими данными
           # Устанавливаем поставщика
           supplier_idx = edit_dialog.supplier_combo.findData(order_data[0])
           if supplier_idx >= 0:
               edit_dialog.supplier_combo.setCurrentIndex(supplier_idx)
           
           # Заполняем таблицу товаров
           for item in order_items:
               row = edit_dialog.order_items_table.rowCount()
               edit_dialog.order_items_table.insertRow(row)
               
               edit_dialog.order_items_table.setItem(row, 0, QTableWidgetItem(str(item[1])))  # product_id
               edit_dialog.order_items_table.setItem(row, 1, QTableWidgetItem(item[2]))       # product_name
               edit_dialog.order_items_table.setItem(row, 2, QTableWidgetItem(str(item[3])))  # quantity
               edit_dialog.order_items_table.setItem(row, 3, QTableWidgetItem(f"{item[4]:.2f}"))  # unit_price
               edit_dialog.order_items_table.setItem(row, 4, QTableWidgetItem(f"{item[5]:.2f}"))  # total_price
           
           edit_dialog.update_total_amount()
           
           # Если пользователь подтвердил изменения
           if edit_dialog.exec():
               # Получаем обновленные данные
               updated_data = edit_dialog.get_data()
               if not updated_data:
                   return
               
               # Начинаем транзакцию
               try:
                   # Обновляем основную информацию о заказе
                   update_query = """
                       UPDATE orders 
                       SET supplier_id = %s, 
                           total_amount = %s,
                           updated_at = CURRENT_TIMESTAMP
                       WHERE order_id = %s
                   """
                   update_params = (
                       updated_data["supplier_id"],
                       updated_data["total_amount"],
                       order_id
                   )
                   self.db.cursor.execute(update_query, update_params)
                   
                   # Удаляем старые позиции заказа
                   delete_items_query = "DELETE FROM order_items WHERE order_id = %s"
                   self.db.cursor.execute(delete_items_query, (order_id,))
                   
                   # Добавляем новые позиции заказа
                   for item in updated_data["items"]:
                       insert_item_query = """
                           INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                           VALUES (%s, %s, %s, %s, %s)
                       """
                       item_params = (
                           order_id,
                           item["product_id"],
                           item["quantity"],
                           item["unit_price"],
                           item["total_price"]
                       )
                       # Выполнение запроса
                       self.db.cursor.execute(insert_item_query, item_params)
                   
                   # Фиксируем транзакцию
                   self.db.conn.commit()
                   # Обновление списка заказов
                   self.load_orders()
                   # Отображение сообщения об успехе
                   QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
               except Exception as tx_error:
                   # Откатываем изменения при ошибке
                   self.db.conn.rollback()
                   # Логирование ошибки
                   logging.error(f"Ошибка транзакции в редактировании заказа: {str(tx_error)}")
                   # Отображение сообщения об ошибке
                   QMessageBox.critical(self, "Ошибка транзакции", f"Не удалось обновить заказ: {str(tx_error)}")
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
            export_format = export_data["format"]
            
            if not file_path:
                # Отображение предупреждения, если путь не выбран
                QMessageBox.warning(self, "Внимание", "Выберите путь для сохранения файла")
                return

            try:
                # Получение текста поиска и выбранного статуса
                search_text = self.search.text()
                status_filter = self.status_filter.currentData()
                
                # Базовый SQL-запрос
                query = """
                    SELECT o.order_date, s.supplier_name, o.total_amount, 
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

                # Заголовки для экспорта
                headers = ["Дата", "Поставщик", "Сумма", "Статус", "Обновлено"]
                
                # Создание объекта для экспорта
                from data_export import DataExporter
                exporter = DataExporter(self)
                
                # Экспорт в зависимости от выбранного формата
                if "Excel" in export_format:
                    success = exporter.export_to_excel(
                        query=query,
                        params=params,
                        filename=file_path,
                        headers=headers,
                        sheet_name="Заказы"
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
                        title="Отчет по заказам"
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
                logging.error(f"Ошибка экспорта заказов: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте данных: {str(e)}")

    def create_purchase_order(self):
         """Создает новый заказ поставщику через диалог."""
         try:
             dialog = CreatePurchaseOrderDialog(self.db, self) # Pass db and parent
             if dialog.exec() == QDialog.DialogCode.Accepted:
                 data = dialog.get_data()
                 if not data:
                     # Dialog already showed specific error, just return
                     return

                 supplier_id = data['supplier_id']
                 items_data = data['items']
                 total_amount = data['total_amount']

                 # Use transaction for order + items insertion
                 order_id = None
                 try:
                     # 1. Create order entry
                     order_query = """
                         INSERT INTO orders (order_date, supplier_id, total_amount, status)
                         VALUES (CURRENT_DATE, %s, %s, 'в обработке')
                         RETURNING order_id
                     """
                     # Use execute_query which handles commit/rollback on its own for single query
                     # We need manual control here for transaction
                     self.db.cursor.execute(order_query, (supplier_id, total_amount))
                     result = self.db.cursor.fetchone()
                     if not result:
                         raise Exception("Не удалось получить ID созданного заказа.")
                     order_id = result[0]

                     # 2. Create order_items entries
                     item_query = """
                         INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                         VALUES (%s, %s, %s, %s, %s)
                     """
                     items_to_insert = [
                         (order_id, item['product_id'], item['quantity'], item['unit_price'], item['total_price'])
                         for item in items_data
                     ]
                     # executemany doesn't return anything useful here
                     self.db.cursor.executemany(item_query, items_to_insert)

                     # If all inserts succeeded, commit the transaction
                     self.db.conn.commit()
                     self.load_orders() # Refresh the orders list
                     QMessageBox.information(self, "Успех", f"Заказ ID {order_id} успешно создан!")

                 except Exception as transaction_error:
                     # Rollback transaction on any error during insert
                     self.db.conn.rollback()
                     logging.error(f"Ошибка транзакции при создании заказа: {transaction_error}")
                     QMessageBox.critical(self, "Ошибка транзакции", f"Не удалось создать заказ (ID заказа={order_id}): {transaction_error}")

         except Exception as dialog_error:
              logging.error(f"Ошибка диалога создания заказа: {dialog_error}")
              QMessageBox.critical(self, "Ошибка", f"Ошибка при создании заказа: {dialog_error}")

    def view_order_details(self):
        """Показывает детальную информацию о заказе в отдельном диалоге."""
        try:
            selected_row = self.orders_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Внимание", "Выберите заказ для просмотра деталей.")
                return

            # Получаем ID заказа
            order_id_item = self.orders_table.item(selected_row, 0)
            if not order_id_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID заказа.")
                return
                
            order_id = int(order_id_item.text())
            
            # Запрашиваем полную информацию о заказе с присоединением имени поставщика
            query_order = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, o.status, o.created_at, o.updated_at
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                WHERE o.order_id = %s
            """
            self.db.cursor.execute(query_order, (order_id,))
            order_details = self.db.cursor.fetchone()
            
            if not order_details:
                QMessageBox.critical(self, "Ошибка", f"Информация о заказе ID {order_id} не найдена.")
                return
                
            # Запрашиваем позиции заказа с названиями товаров
            query_items = """
                SELECT oi.order_item_id, p.product_name, oi.quantity, oi.unit_price, oi.total_price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
            """
            self.db.cursor.execute(query_items, (order_id,))
            order_items = self.db.cursor.fetchall()
            
            # Создаем диалог для отображения деталей
            details_dialog = QDialog(self)
            details_dialog.setWindowTitle(f"Детали заказа №{order_id}")
            details_dialog.setMinimumSize(600, 500)
            
            layout = QVBoxLayout(details_dialog)
            
            # Заголовок заказа
            heading_layout = QVBoxLayout()
            
            # Основная информация
            order_date = QLabel(f"<b>Дата заказа:</b> {order_details[1]}")
            supplier = QLabel(f"<b>Поставщик:</b> {order_details[2]}")
            status = QLabel(f"<b>Статус:</b> {order_details[4]}")
            total = QLabel(f"<b>Общая сумма:</b> {order_details[3]}")
            
            heading_layout.addWidget(QLabel(f"<h2>Заказ №{order_id}</h2>"))
            heading_layout.addWidget(order_date)
            heading_layout.addWidget(supplier)
            heading_layout.addWidget(status)
            heading_layout.addWidget(total)
            
            # Метаданные
            created_updated = QLabel(f"<small>Создан: {order_details[5]} | Обновлен: {order_details[6]}</small>")
            heading_layout.addWidget(created_updated)
            
            layout.addLayout(heading_layout)
            
            # Таблица позиций заказа
            layout.addWidget(QLabel("<h3>Позиции заказа:</h3>"))
            
            items_table = QTableWidget()
            items_table.setColumnCount(5)
            items_table.setHorizontalHeaderLabels(["ID", "Товар", "Количество", "Цена за ед.", "Итого"])
            items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            
            # Заполняем таблицу
            items_table.setRowCount(len(order_items))
            for row, item in enumerate(order_items):
                for col, value in enumerate(item):
                    table_item = QTableWidgetItem(str(value))
                    table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    items_table.setItem(row, col, table_item)
            
            layout.addWidget(items_table)
            
            # Кнопка закрытия
            btn_close = QPushButton("Закрыть")
            btn_close.clicked.connect(details_dialog.close)
            btn_close.setFixedWidth(100)
            
            # Кнопка экспорта в PDF
            btn_export_pdf = QPushButton("Экспорт в PDF")
            btn_export_pdf.clicked.connect(lambda: self.export_order_details_to_pdf(order_id, order_details, order_items))
            btn_export_pdf.setFixedWidth(150)
            
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(btn_export_pdf)
            button_layout.addWidget(btn_close)
            
            layout.addLayout(button_layout)
            
            # Отображаем диалог
            details_dialog.exec()
            
        except Exception as e:
            logging.error(f"Ошибка отображения деталей заказа: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось отобразить детали заказа: {str(e)}")

    def export_order_details_to_pdf(self, order_id, order_details, order_items):
        """Экспортирует детали заказа в PDF файл."""
        try:
            # Импортируем необходимый класс для экспорта
            from data_export import DataExporter
            
            # Создаем экспортер
            exporter = DataExporter(self)
            
            # Используем метод export_order_details_to_pdf из класса DataExporter
            exporter.export_order_details_to_pdf(order_id, order_details, order_items)
            
        except Exception as e:
            logging.error(f"Ошибка при экспорте деталей заказа в PDF: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать детали заказа: {str(e)}")

    def show_order_context_menu(self, position):
        """Показывает контекстное меню для строки заказа."""
        selected_rows = self.orders_table.selectionModel().selectedRows()
        if not selected_rows:
            return # Don't show menu if no row selected

        try:
            menu = QMenu()
            change_status_action = menu.addAction("Изменить статус")
            change_status_action.triggered.connect(self.change_order_status)
            
            # Добавляем пункт просмотра деталей заказа
            view_details_action = menu.addAction("Просмотр деталей")
            view_details_action.triggered.connect(self.view_order_details)
            
            menu.exec(self.orders_table.viewport().mapToGlobal(position))
        except Exception as e:
            logging.error(f"Ошибка контекстного меню заказа: {str(e)}")

    def change_order_status(self):
        """Изменяет статус выбранного заказа."""
        try:
            selected_row = self.orders_table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Внимание", "Выберите заказ для изменения статуса.")
                return

            # Get order ID and current status
            order_id_item = self.orders_table.item(selected_row, 0)
            current_status_item = self.orders_table.item(selected_row, 4)

            if not order_id_item or not current_status_item:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить данные заказа.")
                return

            order_id = int(order_id_item.text())
            current_status = current_status_item.text()
            
            # Логируем полученные данные
            logging.debug(f"Изменение статуса заказа ID: {order_id}, текущий статус: {current_status}")

            # Get list of valid statuses from database (or hardcode them)
            valid_statuses = ['в обработке', 'доставлен', 'отменен']
            # Remove current status from options
            valid_statuses.remove(current_status)

            # Simple QInputDialog to select new status (can replace with custom dialog)
            new_status, ok = QInputDialog.getItem(
                self, "Изменить статус", f"Выберите новый статус для заказа #{order_id}:",
                valid_statuses, 0, False
            )

            if ok and new_status != current_status:
                # Особая обработка для статуса 'доставлен'
                if new_status == 'доставлен' and current_status == 'в обработке':
                    # Показываем подтверждение
                    confirm = QMessageBox.question(
                        self, 
                        "Подтверждение доставки", 
                        "При смене статуса на 'доставлен' будут автоматически обновлены остатки на складе. Продолжить?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    
                    if confirm != QMessageBox.StandardButton.Yes:
                        return
                    
                    # Логируем SQL-запрос перед выполнением    
                    query = "UPDATE orders SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE order_id = %s"
                    logging.debug(f"SQL запрос: {query}, параметры: {(new_status, order_id)}")
                    
                    # Обновляем статус, остальное будет сделано триггером базы данных
                    if self.db.execute_query(query, (new_status, order_id), self):
                        self.load_orders() # Перезагружаем данные
                        QMessageBox.information(
                            self, 
                            "Успех", 
                            f"Статус заказа ID {order_id} обновлен на '{new_status}'!\n"
                            f"Остатки на складе автоматически обновлены."
                        )
                    else:
                        QMessageBox.critical(self, "Ошибка", f"Ошибка обновления статуса заказа ID {order_id}")
                else:
                    # Логируем SQL-запрос перед выполнением
                    query = "UPDATE orders SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE order_id = %s"
                    logging.debug(f"SQL запрос: {query}, параметры: {(new_status, order_id)}")
                    
                    # Стандартное обновление статуса
                    if self.db.execute_query(query, (new_status, order_id), self):
                        self.load_orders() # Reload orders to reflect change
                        QMessageBox.information(self, "Успех", f"Статус заказа ID {order_id} обновлен на '{new_status}'!")
                    else:
                        QMessageBox.critical(self, "Ошибка", f"Ошибка обновления статуса заказа ID {order_id}")

        except Exception as e:
            logging.error(f"Ошибка изменения статуса заказа: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при изменении статуса: {str(e)}")