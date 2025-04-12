from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddSupplierDialog, ConfirmDialog, EmailDialog

class SuppliersTab(QWidget):
    """
    Tab for managing suppliers in the warehouse management system.
    """

    def __init__(self, db):
        """
        Initialize the suppliers tab.

        Args:
            db: Database object for supplier operations
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_suppliers()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()

        # Top panel with control buttons
        top_panel = QHBoxLayout()

        # Control buttons
        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_email = QPushButton("Отправить письмо")

        # Search field
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        # Add a stretching element
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add elements to top panel
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_delete)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.btn_email)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Table for displaying suppliers
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(5)
        self.suppliers_table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Контактное лицо", "Телефон", "Email"
        ])
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.suppliers_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Bottom panel with additional functions
        bottom_panel = QHBoxLayout()

        # Left side of bottom panel - buttons with icons
        left_button_panel = QHBoxLayout()

        # Refresh button
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Orders button
        self.btn_orders = QPushButton("Заказы поставщика")
        self.btn_orders.setIcon(QIcon.fromTheme("document-properties"))

        # Add buttons to left panel
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_orders)
        left_button_panel.addStretch()

        # Right side of bottom panel - export button
        right_button_panel = QHBoxLayout()
        
        # Supplier count
        self.supplier_count_label = QLabel("Всего поставщиков: 0")
        
        # Export button
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Add elements to right panel
        right_button_panel.addWidget(self.supplier_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Assemble bottom panel from left and right parts
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Assemble main interface
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.suppliers_table)
        main_layout.addLayout(bottom_panel)

        self.setLayout(main_layout)

        # Connect event handlers
        self.btn_add.clicked.connect(self.add_supplier)
        self.btn_delete.clicked.connect(self.delete_supplier)
        self.btn_edit.clicked.connect(self.edit_supplier)
        self.btn_email.clicked.connect(self.send_email)
        self.btn_refresh.clicked.connect(self.load_suppliers)
        self.btn_orders.clicked.connect(self.show_supplier_orders)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_suppliers(self):
        """Load suppliers from database and display in table."""
        try:
            query = """
                SELECT supplier_id, supplier_name, contact_person, phone_number, email
                FROM suppliers
                ORDER BY supplier_name
            """
            suppliers = self.db.fetch_all(query)

            self.suppliers_table.setRowCount(len(suppliers))

            for row_idx, supplier in enumerate(suppliers):
                for col_idx, data in enumerate(supplier):
                    item = QTableWidgetItem(str(data) if data else "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.suppliers_table.setItem(row_idx, col_idx, item)
            
            # Update supplier count
            self.supplier_count_label.setText(f"Всего поставщиков: {len(suppliers)}")
            
        except Exception as e:
            logging.error(f"Error loading suppliers: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о поставщиках")

    def handle_search(self):
        """Handle supplier search by typed text."""
        try:
            search_text = self.search.text()

            query = """
                SELECT supplier_id, supplier_name, contact_person, phone_number, email
                FROM suppliers
                WHERE supplier_name ILIKE %s 
                   OR contact_person ILIKE %s 
                   OR phone_number LIKE %s
                   OR email ILIKE %s
                ORDER BY supplier_name
            """
            search_param = f"%{search_text}%"
            suppliers = self.db.fetch_all(query, (search_param, search_param, search_param, search_param))

            self.suppliers_table.setRowCount(len(suppliers))

            for row_idx, supplier in enumerate(suppliers):
                for col_idx, data in enumerate(supplier):
                    item = QTableWidgetItem(str(data) if data else "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.suppliers_table.setItem(row_idx, col_idx, item)
                    
            # Update supplier count for search results
            self.supplier_count_label.setText(f"Найдено поставщиков: {len(suppliers)}")
            
        except Exception as e:
            logging.error(f"Error searching suppliers: {str(e)}")

    def add_supplier(self):
        """Show dialog to add a new supplier."""
        dialog = AddSupplierDialog(self, self.db)
        if dialog.exec():
            supplier_data = dialog.get_supplier_data()
            try:
                query = """
                    INSERT INTO suppliers (supplier_name, contact_person, phone_number, email)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    supplier_data["name"],
                    supplier_data["contact"],
                    supplier_data["phone"],
                    supplier_data["email"]
                )
                success = self.db.execute_query(query, params)
                if success:
                    self.load_suppliers()
                    QMessageBox.information(self, "Успех", "Поставщик успешно добавлен")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить поставщика")
            except Exception as e:
                logging.error(f"Error adding supplier: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить поставщика: {str(e)}")

    def delete_supplier(self):
        """Delete selected supplier."""
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для удаления")
            return

        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()
        supplier_name = self.suppliers_table.item(row, 1).text()

        # Check if supplier has associated orders
        try:
            check_query = "SELECT COUNT(*) FROM orders WHERE supplier_id = %s"
            count = self.db.fetch_one(check_query, (supplier_id,))
            
            if count and count[0] > 0:
                QMessageBox.warning(
                    self, 
                    "Внимание", 
                    f"Поставщик '{supplier_name}' имеет связанные заказы и не может быть удален."
                )
                return
        except Exception as e:
            logging.error(f"Error checking supplier orders: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось проверить связанные заказы: {str(e)}")
            return

        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить поставщика:\n{supplier_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                query = "DELETE FROM suppliers WHERE supplier_id = %s"
                success = self.db.execute_query(query, (supplier_id,))
                if success:
                    self.load_suppliers()
                    QMessageBox.information(self, "Успех", "Поставщик успешно удален")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить поставщика")
            except Exception as e:
                logging.error(f"Error deleting supplier: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить поставщика: {str(e)}")

    def edit_supplier(self):
        """Edit selected supplier."""
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для редактирования")
            return

        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()

        try:
            query = """
                SELECT supplier_name, contact_person, phone_number, email 
                FROM suppliers 
                WHERE supplier_id = %s
            """
            supplier = self.db.fetch_one(query, (supplier_id,))
            
            if supplier:
                dialog = AddSupplierDialog(self, self.db)
                dialog.setWindowTitle("Редактировать поставщика")
                
                # Fill dialog with current supplier data
                dialog.name_input.setText(supplier[0] if supplier[0] else "")
                dialog.contact_input.setText(supplier[1] if supplier[1] else "")
                dialog.phone_input.setText(supplier[2] if supplier[2] else "")
                dialog.email_input.setText(supplier[3] if supplier[3] else "")

                if dialog.exec():
                    updated_data = dialog.get_supplier_data()
                    update_query = """
                        UPDATE suppliers 
                        SET supplier_name = %s, 
                            contact_person = %s, 
                            phone_number = %s, 
                            email = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE supplier_id = %s
                    """
                    update_params = (
                        updated_data["name"],
                        updated_data["contact"],
                        updated_data["phone"],
                        updated_data["email"],
                        supplier_id
                    )
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        self.load_suppliers()
                        QMessageBox.information(self, "Успех", "Данные поставщика успешно обновлены")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные поставщика")
        except Exception as e:
            logging.error(f"Error editing supplier: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать поставщика: {str(e)}")

    def send_email(self):
        """Send email to selected supplier."""
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для отправки письма")
            return

        row = selected_rows[0].row()
        supplier_name = self.suppliers_table.item(row, 1).text()
        email = self.suppliers_table.item(row, 4).text()
        
        if not email:
            QMessageBox.warning(self, "Внимание", "У выбранного поставщика не указан email")
            return
            
        dialog = EmailDialog(self)
        dialog.to_input.setText(email)
        dialog.subject_input.setText(f"Запрос от компании \"WareHouse\"")
        
        if dialog.exec():
            # This would actually send an email in a real application
            QMessageBox.information(self, "Отправка письма", f"Письмо для {supplier_name} успешно отправлено")

    def show_supplier_orders(self):
        """Show orders for selected supplier."""
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для просмотра заказов")
            return

        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()
        supplier_name = self.suppliers_table.item(row, 1).text()
        
        try:
            query = """
                SELECT order_id, order_date, total_amount, status
                FROM orders
                WHERE supplier_id = %s
                ORDER BY order_date DESC
            """
            orders = self.db.fetch_all(query, (supplier_id,))
            
            if not orders:
                QMessageBox.information(self, "Заказы поставщика", f"У поставщика {supplier_name} нет заказов")
                return
                
            # Format details text
            details_text = f"Заказы поставщика: {supplier_name}\n\n"
            details_text += "ID | Дата | Сумма | Статус\n"
            details_text += "--------------------------------\n"
            
            for order in orders:
                details_text += f"{order[0]} | {order[1]} | {order[2]}₽ | {order[3]}\n"
                
            QMessageBox.information(self, "Заказы поставщика", details_text)
            
        except Exception as e:
            logging.error(f"Error showing supplier orders: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы поставщика: {str(e)}")

    def export_data(self):
        """Export suppliers data."""
        # Simple implementation - in a real app would use export functionality
        QMessageBox.information(self, "Экспорт", "Функция экспорта пока не реализована") 