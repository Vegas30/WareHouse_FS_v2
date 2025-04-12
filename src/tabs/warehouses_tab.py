from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QSpacerItem, QSizePolicy, QDialog, QFormLayout, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddWarehouseDialog, ConfirmDialog

class WarehousesTab(QWidget):
    """
    Tab for managing warehouses in the warehouse management system.
    """

    def __init__(self, db):
        """
        Initialize the warehouses tab.

        Args:
            db: Database object for warehouse operations
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_warehouses()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()

        # Top panel with control buttons
        top_panel = QHBoxLayout()

        # Control buttons
        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_edit = QPushButton("Редактировать")

        # Search field
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        # Add a stretching element
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add elements to top panel
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_delete)
        top_panel.addWidget(self.btn_edit)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Table for displaying warehouses
        self.warehouses_table = QTableWidget()
        self.warehouses_table.setColumnCount(4)
        self.warehouses_table.setHorizontalHeaderLabels([
            "ID", "Название", "Местоположение", "Вместимость"
        ])
        self.warehouses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.warehouses_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Bottom panel with additional functions
        bottom_panel = QHBoxLayout()

        # Left side of bottom panel - buttons with icons
        left_button_panel = QHBoxLayout()

        # Refresh button
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Stock button
        self.btn_stock = QPushButton("Запасы на складе")
        self.btn_stock.setIcon(QIcon.fromTheme("document-properties"))

        # Add buttons to left panel
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_stock)
        left_button_panel.addStretch()

        # Right side of bottom panel - export button and capacity info
        right_button_panel = QHBoxLayout()
        
        # Warehouse count
        self.warehouse_count_label = QLabel("Всего складов: 0")
        
        # Export button
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Add elements to right panel
        right_button_panel.addWidget(self.warehouse_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Assemble bottom panel from left and right parts
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Assemble main interface
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.warehouses_table)
        main_layout.addLayout(bottom_panel)

        self.setLayout(main_layout)

        # Connect event handlers
        self.btn_add.clicked.connect(self.add_warehouse)
        self.btn_delete.clicked.connect(self.delete_warehouse)
        self.btn_edit.clicked.connect(self.edit_warehouse)
        self.btn_refresh.clicked.connect(self.load_warehouses)
        self.btn_stock.clicked.connect(self.show_warehouse_stock)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_warehouses(self):
        """Load warehouses from database and display in table."""
        try:
            query = """
                SELECT warehouse_id, warehouse_name, location, capacity
                FROM warehouses
                ORDER BY warehouse_name
            """
            warehouses = self.db.fetch_all(query)

            self.warehouses_table.setRowCount(len(warehouses))

            for row_idx, warehouse in enumerate(warehouses):
                for col_idx, data in enumerate(warehouse):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.warehouses_table.setItem(row_idx, col_idx, item)
                    
            # Update warehouse count
            self.warehouse_count_label.setText(f"Всего складов: {len(warehouses)}")
            
        except Exception as e:
            logging.error(f"Error loading warehouses: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о складах")

    def handle_search(self):
        """Handle warehouse search by typed text."""
        try:
            search_text = self.search.text()

            query = """
                SELECT warehouse_id, warehouse_name, location, capacity
                FROM warehouses
                WHERE warehouse_name ILIKE %s OR location ILIKE %s
                ORDER BY warehouse_name
            """
            search_param = f"%{search_text}%"
            warehouses = self.db.fetch_all(query, (search_param, search_param))

            self.warehouses_table.setRowCount(len(warehouses))

            for row_idx, warehouse in enumerate(warehouses):
                for col_idx, data in enumerate(warehouse):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.warehouses_table.setItem(row_idx, col_idx, item)
                    
            # Update warehouse count for search results
            self.warehouse_count_label.setText(f"Найдено складов: {len(warehouses)}")
            
        except Exception as e:
            logging.error(f"Error searching warehouses: {str(e)}")

    def add_warehouse(self):
        """Show dialog to add a new warehouse."""
        dialog = AddWarehouseDialog(self, self.db)
        if dialog.exec():
            warehouse_data = dialog.get_warehouse_data()
            try:
                query = """
                    INSERT INTO warehouses (warehouse_name, location, capacity)
                    VALUES (%s, %s, %s)
                """
                params = (
                    warehouse_data["name"],
                    warehouse_data["location"],
                    warehouse_data["capacity"]
                )
                success = self.db.execute_query(query, params)
                if success:
                    self.load_warehouses()
                    QMessageBox.information(self, "Успех", "Склад успешно добавлен")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить склад")
            except Exception as e:
                logging.error(f"Error adding warehouse: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить склад: {str(e)}")

    def delete_warehouse(self):
        """Delete selected warehouse."""
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите склад для удаления")
            return

        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()
        warehouse_name = self.warehouses_table.item(row, 1).text()

        # Check if warehouse has associated stock
        try:
            check_query = "SELECT COUNT(*) FROM stock WHERE warehouse_id = %s"
            count = self.db.fetch_one(check_query, (warehouse_id,))
            
            if count and count[0] > 0:
                QMessageBox.warning(
                    self, 
                    "Внимание", 
                    f"Склад '{warehouse_name}' содержит товары и не может быть удален."
                )
                return
        except Exception as e:
            logging.error(f"Error checking warehouse stock: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось проверить содержимое склада: {str(e)}")
            return

        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить склад:\n{warehouse_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                query = "DELETE FROM warehouses WHERE warehouse_id = %s"
                success = self.db.execute_query(query, (warehouse_id,))
                if success:
                    self.load_warehouses()
                    QMessageBox.information(self, "Успех", "Склад успешно удален")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить склад")
            except Exception as e:
                logging.error(f"Error deleting warehouse: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить склад: {str(e)}")

    def edit_warehouse(self):
        """Edit selected warehouse."""
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите склад для редактирования")
            return

        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()

        try:
            query = """
                SELECT warehouse_name, location, capacity 
                FROM warehouses 
                WHERE warehouse_id = %s
            """
            warehouse = self.db.fetch_one(query, (warehouse_id,))
            
            if warehouse:
                dialog = AddWarehouseDialog(self, self.db)
                dialog.setWindowTitle("Редактировать склад")
                
                # Fill dialog with current warehouse data
                dialog.name_input.setText(warehouse[0])
                dialog.location_input.setText(warehouse[1])
                dialog.capacity_input.setValue(int(warehouse[2]))

                if dialog.exec():
                    updated_data = dialog.get_warehouse_data()
                    update_query = """
                        UPDATE warehouses 
                        SET warehouse_name = %s, 
                            location = %s, 
                            capacity = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE warehouse_id = %s
                    """
                    update_params = (
                        updated_data["name"],
                        updated_data["location"],
                        updated_data["capacity"],
                        warehouse_id
                    )
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        self.load_warehouses()
                        QMessageBox.information(self, "Успех", "Данные склада успешно обновлены")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные склада")
        except Exception as e:
            logging.error(f"Error editing warehouse: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать склад: {str(e)}")

    def show_warehouse_stock(self):
        """Show stock items stored in selected warehouse."""
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите склад для просмотра запасов")
            return

        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()
        warehouse_name = self.warehouses_table.item(row, 1).text()
        
        try:
            query = """
                SELECT p.product_name, s.quantity, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE s.warehouse_id = %s
                ORDER BY p.product_name
            """
            stock_items = self.db.fetch_all(query, (warehouse_id,))
            
            if not stock_items:
                QMessageBox.information(self, "Запасы на складе", f"На складе {warehouse_name} нет товаров")
                return
                
            # Format details text
            details_text = f"Товары на складе: {warehouse_name}\n\n"
            details_text += "Товар | Количество | Категория | Цена\n"
            details_text += "--------------------------------\n"
            
            total_items = 0
            total_value = 0
            
            for item in stock_items:
                product_name, quantity, category, price = item
                item_value = quantity * price
                total_items += quantity
                total_value += item_value
                
                details_text += f"{product_name} | {quantity} | {category} | {price}₽\n"
                
            details_text += "--------------------------------\n"
            details_text += f"Всего товаров: {total_items}\n"
            details_text += f"Общая стоимость: {total_value}₽"
                
            QMessageBox.information(self, "Запасы на складе", details_text)
            
        except Exception as e:
            logging.error(f"Error showing warehouse stock: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить запасы склада: {str(e)}")

    def export_data(self):
        """Export warehouses data."""
        # Simple implementation - in a real app would use export functionality
        QMessageBox.information(self, "Экспорт", "Функция экспорта пока не реализована") 