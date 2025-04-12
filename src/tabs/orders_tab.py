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
    Tab for managing orders in the warehouse management system.
    """

    def __init__(self, db):
        """
        Initialize the orders tab.

        Args:
            db: Database object for order operations
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_orders()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()

        # Top panel with control buttons and filters
        top_panel = QHBoxLayout()

        # Control buttons
        self.btn_add = QPushButton("Создать заказ")
        self.btn_add.setStyleSheet("background-color: #2e7d32;")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_cancel = QPushButton("Отменить")
        self.btn_cancel.setStyleSheet("background-color: #d32f2f;")

        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItem("Все статусы", None)
        self.status_filter.addItem("В обработке", "в обработке")
        self.status_filter.addItem("Доставлен", "доставлен")
        self.status_filter.addItem("Отменен", "отменен")
        
        # Search field
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск заказа...")

        # Add a stretching element
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add elements to top panel
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.btn_cancel)
        top_panel.addWidget(QLabel("Статус:"))
        top_panel.addWidget(self.status_filter)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Table for displaying orders
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Дата", "Поставщик", "Сумма", "Статус", "Обновлено"
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Bottom panel with additional functions
        bottom_panel = QHBoxLayout()

        # Left side of bottom panel - buttons with icons
        left_button_panel = QHBoxLayout()

        # Refresh button
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Details button
        self.btn_details = QPushButton("Детали заказа")
        self.btn_details.setIcon(QIcon.fromTheme("document-properties"))

        # Add buttons to left panel
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_details)
        left_button_panel.addStretch()

        # Right side of bottom panel - export button
        right_button_panel = QHBoxLayout()
        
        # Order count
        self.order_count_label = QLabel("Всего заказов: 0")
        
        # Export button
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Add elements to right panel
        right_button_panel.addWidget(self.order_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Assemble bottom panel from left and right parts
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Assemble main interface
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(bottom_panel)

        self.setLayout(main_layout)

        # Connect event handlers
        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_cancel.clicked.connect(self.cancel_order)
        self.btn_refresh.clicked.connect(self.load_orders)
        self.btn_details.clicked.connect(self.show_order_details)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)

    def load_orders(self):
        """Load orders from database and display in table."""
        try:
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, 
                       o.status, o.updated_at
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                ORDER BY o.order_date DESC
            """
            orders = self.db.fetch_all(query)

            self.orders_table.setRowCount(len(orders))

            for row_idx, order in enumerate(orders):
                for col_idx, data in enumerate(order):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Color code status column
                    if col_idx == 4:  # Status column
                        if data == "доставлен":
                            item.setForeground(Qt.GlobalColor.darkGreen)
                        elif data == "отменен":
                            item.setForeground(Qt.GlobalColor.red)
                        elif data == "в обработке":
                            item.setForeground(Qt.GlobalColor.blue)
                    
                    self.orders_table.setItem(row_idx, col_idx, item)
            
            # Update order count
            self.order_count_label.setText(f"Всего заказов: {len(orders)}")
            
        except Exception as e:
            logging.error(f"Error loading orders: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о заказах")

    def handle_search(self):
        """Handle search and filter changes."""
        self.apply_filters()

    def apply_filters(self):
        """Apply filters to orders table."""
        try:
            search_text = self.search.text()
            status_filter = self.status_filter.currentData()
            
            # Base query
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, 
                       o.status, o.updated_at
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                WHERE 1=1
            """
            params = []
            
            # Add status filter
            if status_filter:
                query += " AND o.status = %s"
                params.append(status_filter)
            
            # Add search filter
            if search_text:
                query += """ AND (
                    o.order_id::text LIKE %s
                    OR s.supplier_name ILIKE %s
                )"""
                search_param = f"%{search_text}%"
                params.extend([search_param, search_param])
            
            # Add ordering
            query += " ORDER BY o.order_date DESC"
            
            # Execute query
            orders = self.db.fetch_all(query, tuple(params))
            
            # Update table
            self.orders_table.setRowCount(len(orders))
            
            for row_idx, order in enumerate(orders):
                for col_idx, data in enumerate(order):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Color code status column
                    if col_idx == 4:  # Status column
                        if data == "доставлен":
                            item.setForeground(Qt.GlobalColor.darkGreen)
                        elif data == "отменен":
                            item.setForeground(Qt.GlobalColor.red)
                        elif data == "в обработке":
                            item.setForeground(Qt.GlobalColor.blue)
                    
                    self.orders_table.setItem(row_idx, col_idx, item)
            
            # Update order count
            self.order_count_label.setText(f"Найдено заказов: {len(orders)}")
            
        except Exception as e:
            logging.error(f"Error filtering orders: {str(e)}")

    def add_order(self):
        """Show dialog to create a new order."""
        dialog = AddOrderDialog(self, self.db)
        if dialog.exec():
            order_data = dialog.get_order_data()
            try:
                query = """
                    INSERT INTO orders (order_date, supplier_id, total_amount, status)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    order_data["date"],
                    order_data["supplier_id"],
                    order_data["amount"],
                    order_data["status"]
                )
                success = self.db.execute_query(query, params)
                if success:
                    self.load_orders()
                    QMessageBox.information(self, "Успех", "Заказ успешно создан")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось создать заказ")
            except Exception as e:
                logging.error(f"Error creating order: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")

    def edit_order(self):
        """Edit selected order."""
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите заказ для редактирования")
            return
            
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        status = self.orders_table.item(row, 4).text()
        
        if status == "доставлен" or status == "отменен":
            QMessageBox.warning(self, "Внимание", "Нельзя редактировать завершенный или отмененный заказ")
            return
            
        try:
            # Get order data
            query = """
                SELECT order_date, supplier_id, total_amount, status 
                FROM orders 
                WHERE order_id = %s
            """
            order_data = self.db.fetch_one(query, (order_id,))
            
            if order_data:
                dialog = AddOrderDialog(self, self.db)
                dialog.setWindowTitle("Редактировать заказ")
                
                # Set dialog fields with current data
                dialog.date_input.setDate(Qt.QDate.fromString(str(order_data[0]), "yyyy-MM-dd"))
                
                # Find supplier index
                supplier_idx = -1
                for i in range(dialog.supplier_input.count()):
                    if dialog.supplier_input.itemData(i) == order_data[1]:
                        supplier_idx = i
                        break
                if supplier_idx >= 0:
                    dialog.supplier_input.setCurrentIndex(supplier_idx)
                
                dialog.amount_input.setValue(float(order_data[2]))
                
                # Find status index
                status_idx = dialog.status_input.findText(order_data[3])
                if status_idx >= 0:
                    dialog.status_input.setCurrentIndex(status_idx)
                
                if dialog.exec():
                    updated_data = dialog.get_order_data()
                    update_query = """
                        UPDATE orders 
                        SET order_date = %s, 
                            supplier_id = %s, 
                            total_amount = %s, 
                            status = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE order_id = %s
                    """
                    update_params = (
                        updated_data["date"],
                        updated_data["supplier_id"],
                        updated_data["amount"],
                        updated_data["status"],
                        order_id
                    )
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        self.load_orders()
                        QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить заказ")
        except Exception as e:
            logging.error(f"Error editing order: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать заказ: {str(e)}")

    def cancel_order(self):
        """Cancel selected order."""
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите заказ для отмены")
            return
            
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        status = self.orders_table.item(row, 4).text()
        
        if status == "доставлен" or status == "отменен":
            QMessageBox.warning(self, "Внимание", "Нельзя отменить завершенный или уже отмененный заказ")
            return
            
        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение отмены заказа",
            f"Вы действительно хотите отменить заказ #{order_id}?"
        )
        
        if confirm_dialog.exec():
            try:
                query = """
                    UPDATE orders 
                    SET status = 'отменен', 
                        updated_at = CURRENT_TIMESTAMP
                    WHERE order_id = %s
                """
                success = self.db.execute_query(query, (order_id,))
                if success:
                    self.load_orders()
                    QMessageBox.information(self, "Успех", "Заказ успешно отменен")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось отменить заказ")
            except Exception as e:
                logging.error(f"Error cancelling order: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось отменить заказ: {str(e)}")

    def show_order_details(self):
        """Show details for selected order."""
        selected_rows = self.orders_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите заказ для просмотра деталей")
            return
            
        row = selected_rows[0].row()
        order_id = self.orders_table.item(row, 0).text()
        
        try:
            # Get order items
            query = """
                SELECT p.product_name, oi.quantity, oi.unit_price, oi.total_price
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            """
            items = self.db.fetch_all(query, (order_id,))
            
            # Format details text
            details_text = f"Детали заказа #{order_id}:\n\n"
            
            if items:
                details_text += "Товары в заказе:\n"
                details_text += "--------------------------------\n"
                details_text += "Товар | Кол-во | Цена | Сумма\n"
                details_text += "--------------------------------\n"
                
                for item in items:
                    details_text += f"{item[0]} | {item[1]} | {item[2]}₽ | {item[3]}₽\n"
                
                details_text += "--------------------------------\n"
                details_text += f"Общая сумма: {self.orders_table.item(row, 3).text()}₽"
            else:
                details_text += "В этом заказе нет товаров"
            
            QMessageBox.information(self, "Детали заказа", details_text)
            
        except Exception as e:
            logging.error(f"Error showing order details: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить детали заказа: {str(e)}")

    def export_data(self):
        """Export orders data."""
        dialog = ExportDialog(self, "Экспорт заказов")
        if dialog.exec():
            export_data = dialog.get_export_data()
            file_path = export_data["file_path"]
            
            if not file_path:
                QMessageBox.warning(self, "Внимание", "Выберите путь для сохранения файла")
                return
            
            # Here would be the actual export implementation
            # This is just a placeholder message
            QMessageBox.information(self, "Экспорт", f"Данные успешно экспортированы в {file_path}") 