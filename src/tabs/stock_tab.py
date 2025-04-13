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
from validators import Validator
from visualization import InventoryAnalysisDialog

class StockTab(QWidget):
    """
    Tab for managing stock in the warehouse management system.
    """

    def __init__(self, db):
        """
        Initialize the stock tab.

        Args:
            db: Database object for stock operations
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_stock()
        self.check_low_stock_alert()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()

        # Top panel with control buttons and filters
        top_panel = QHBoxLayout()

        # Control buttons
        self.btn_add = QPushButton("Добавить")
        self.btn_update = QPushButton("Обновить запас")
        self.btn_move = QPushButton("Переместить")

        # Warehouse filter
        self.warehouse_filter = QComboBox()
        self.warehouse_filter.setMinimumWidth(200)
        self.warehouse_filter.addItem("Все склады", None)
        self.load_warehouses()
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.setMinimumWidth(150)
        self.category_filter.addItem("Все категории", None)
        self.load_categories()
        
        # Search field
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск товара...")

        # Add a stretching element
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add elements to top panel
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_update)
        top_panel.addWidget(self.btn_move)
        top_panel.addWidget(QLabel("Склад:"))
        top_panel.addWidget(self.warehouse_filter)
        top_panel.addWidget(QLabel("Категория:"))
        top_panel.addWidget(self.category_filter)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Table for displaying stock
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(7)
        self.stock_table.setHorizontalHeaderLabels([
            "ID", "Товар", "Склад", "Количество", 
            "Последнее пополнение", "Категория", "Цена за ед."
        ])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stock_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Bottom panel with additional functions
        bottom_panel = QHBoxLayout()

        # Left side of bottom panel - buttons with icons
        left_button_panel = QHBoxLayout()

        # Refresh button
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Report button
        self.btn_report = QPushButton("Отчет")
        self.btn_report.setIcon(QIcon.fromTheme("x-office-document"))
        
        # Analysis button
        self.btn_analysis = QPushButton("Анализ запасов")
        self.btn_analysis.setIcon(QIcon.fromTheme("accessories-calculator"))

        # Add buttons to left panel
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_report)
        left_button_panel.addWidget(self.btn_analysis)
        left_button_panel.addStretch()

        # Right side of bottom panel - export buttons and low stock warning
        right_button_panel = QHBoxLayout()
        
        # Low stock warning
        self.low_stock_label = QLabel("Товары с низким запасом: 0")
        self.low_stock_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
        
        # Export buttons
        self.btn_export_csv = QPushButton("Экспорт в CSV")
        self.btn_export_csv.setIcon(QIcon.fromTheme("document-save"))
        
        self.btn_export_excel = QPushButton("Экспорт в Excel")
        self.btn_export_excel.setIcon(QIcon.fromTheme("x-office-spreadsheet"))

        # Add elements to right panel
        right_button_panel.addWidget(self.low_stock_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export_csv)
        right_button_panel.addWidget(self.btn_export_excel)

        # Assemble bottom panel from left and right parts
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Assemble main interface
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.stock_table)
        main_layout.addLayout(bottom_panel)

        self.setLayout(main_layout)

        # Connect event handlers
        self.btn_add.clicked.connect(self.add_stock)
        self.btn_update.clicked.connect(self.update_stock)
        self.btn_move.clicked.connect(self.move_stock)
        self.btn_refresh.clicked.connect(self.load_stock)
        self.btn_report.clicked.connect(self.generate_report)
        self.btn_export_csv.clicked.connect(self.export_to_csv)
        self.btn_export_excel.clicked.connect(self.export_to_excel)
        self.btn_analysis.clicked.connect(self.show_analysis)
        self.search.textChanged.connect(self.handle_search)
        self.warehouse_filter.currentIndexChanged.connect(self.load_stock)
        self.category_filter.currentIndexChanged.connect(self.load_stock)

    def load_warehouses(self):
        """Load warehouses for filter dropdown."""
        try:
            query = "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name"
            warehouses = self.db.fetch_all(query, parent_widget=self)
            
            for warehouse_id, warehouse_name in warehouses:
                self.warehouse_filter.addItem(warehouse_name, warehouse_id)
                
        except Exception as e:
            logging.error(f"Error loading warehouses: {str(e)}")
    
    def load_categories(self):
        """Load product categories for filter dropdown."""
        try:
            query = "SELECT DISTINCT category FROM products ORDER BY category"
            categories = self.db.fetch_all(query, parent_widget=self)
            
            for category in categories:
                self.category_filter.addItem(category[0], category[0])
                
        except Exception as e:
            logging.error(f"Error loading categories: {str(e)}")

    def load_stock(self):
        """Load stock data from database and display in table."""
        try:
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Base query
            query = """
                SELECT s.stock_id, p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Add warehouse filter if selected
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Add category filter if selected
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Add search filter if provided
            if search_text:
                # Sanitize input for search
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Add ordering
            query += " ORDER BY p.product_name"
            
            # Execute query
            stock_data = self.db.fetch_all(query, params, parent_widget=self)

            self.stock_table.setRowCount(len(stock_data))
            
            low_stock_count = 0
            low_stock_threshold = 10  # Configure low stock threshold
            
            for row_idx, stock_item in enumerate(stock_data):
                for col_idx, data in enumerate(stock_item):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    
                    # Highlight low stock items
                    if col_idx == 3 and int(data) < low_stock_threshold:
                        item.setForeground(Qt.GlobalColor.red)
                        low_stock_count += 1
                        
                    self.stock_table.setItem(row_idx, col_idx, item)
            
            # Update low stock warning
            self.low_stock_label.setText(f"Товары с низким запасом: {low_stock_count}")
            
            # Check if low stock alert is needed
            if low_stock_count > 0:
                self.low_stock_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
            else:
                self.low_stock_label.setStyleSheet("color: #2e7d32; font-weight: bold;")
            
        except Exception as e:
            logging.error(f"Error loading stock: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о запасах")

    def handle_search(self):
        """Handle stock search by product name or category."""
        self.load_stock()

    def check_low_stock_alert(self):
        """Check if there are items with critically low stock and show an alert."""
        try:
            # Define critical threshold (can be configurable)
            critical_threshold = 5
            
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE s.quantity < %s
                ORDER BY s.quantity
            """
            
            critical_items = self.db.fetch_all(query, (critical_threshold,), parent_widget=self)
            
            if critical_items:
                alert_message = "Внимание! Критически низкий уровень запасов:\n\n"
                
                for item in critical_items:
                    product_name, warehouse_name, quantity = item
                    alert_message += f"• {product_name} ({warehouse_name}): {quantity} шт.\n"
                
                QMessageBox.warning(self, "Низкий уровень запасов", alert_message)
        
        except Exception as e:
            logging.error(f"Error checking low stock: {str(e)}")

    def add_stock(self):
        """Open dialog to add new stock item."""
        dialog = AddStockDialog(self, self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_stock()

    def update_stock(self):
        """Update stock quantity for selected item."""
        selected_row = self.stock_table.currentRow()
        
        if selected_row >= 0:
            stock_id = self.stock_table.item(selected_row, 0).text()
            product_name = self.stock_table.item(selected_row, 1).text()
            current_quantity = int(self.stock_table.item(selected_row, 3).text())
            
            dialog = UpdateStockDialog(self, product_name, current_quantity)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_quantity = dialog.get_quantity()
                
                try:
                    query = """
                        UPDATE stock 
                        SET quantity = %s, last_restocked = CURRENT_DATE
                        WHERE stock_id = %s
                    """
                    
                    success = self.db.execute_query(query, (new_quantity, stock_id), parent_widget=self)
                    
                    if success:
                        self.load_stock()
                        QMessageBox.information(self, "Успех", "Количество товара обновлено")
                
                except Exception as e:
                    logging.error(f"Error updating stock: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить количество товара")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для обновления")

    def move_stock(self):
        """Move stock from one warehouse to another."""
        selected_row = self.stock_table.currentRow()
        
        if selected_row >= 0:
            stock_id = self.stock_table.item(selected_row, 0).text()
            product_name = self.stock_table.item(selected_row, 1).text()
            source_warehouse = self.stock_table.item(selected_row, 2).text()
            current_quantity = int(self.stock_table.item(selected_row, 3).text())
            
            dialog = MoveStockDialog(self, self.db, product_name, source_warehouse, current_quantity)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                target_warehouse_id, quantity_to_move = dialog.get_move_data()
                
                if quantity_to_move > current_quantity:
                    QMessageBox.warning(self, "Предупреждение", "Нельзя переместить больше товара, чем имеется на складе")
                    return
                
                try:
                    # Get product_id from the selected stock item
                    query = "SELECT product_id FROM stock WHERE stock_id = %s"
                    product_id = self.db.fetch_one(query, (stock_id,), parent_widget=self)[0]
                    
                    # Update source warehouse quantity
                    query = """
                        UPDATE stock 
                        SET quantity = quantity - %s
                        WHERE stock_id = %s
                    """
                    self.db.execute_query(query, (quantity_to_move, stock_id), parent_widget=self)
                    
                    # Check if the product already exists in the target warehouse
                    query = """
                        SELECT stock_id, quantity 
                        FROM stock 
                        WHERE product_id = %s AND warehouse_id = %s
                    """
                    target_stock = self.db.fetch_one(query, (product_id, target_warehouse_id), parent_widget=self)
                    
                    if target_stock:
                        # Product exists in target warehouse, update quantity
                        target_stock_id, target_quantity = target_stock
                        query = """
                            UPDATE stock 
                            SET quantity = quantity + %s
                            WHERE stock_id = %s
                        """
                        self.db.execute_query(query, (quantity_to_move, target_stock_id), parent_widget=self)
                    else:
                        # Product doesn't exist in target warehouse, insert new record
                        query = """
                            INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
                            VALUES (%s, %s, %s, CURRENT_DATE)
                        """
                        self.db.execute_query(query, (product_id, target_warehouse_id, quantity_to_move), parent_widget=self)
                    
                    self.load_stock()
                    QMessageBox.information(self, "Успех", f"Товар успешно перемещен ({quantity_to_move} шт.)")
                
                except Exception as e:
                    logging.error(f"Error moving stock: {str(e)}")
                    QMessageBox.critical(self, "Ошибка", "Не удалось переместить товар")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите товар для перемещения")
    
    def generate_report(self):
        """Generate stock report."""
        try:
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            
            title = "Отчет по запасам"
            message = "Сводная информация по запасам:\n\n"
            
            # Query for total stock value
            value_query = """
                SELECT SUM(p.unit_price * s.quantity) as total_value
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1
            """
            
            # Query for stock by category
            category_query = """
                SELECT p.category, SUM(s.quantity) as total_quantity
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE 1=1
            """
            
            # Query for low stock items
            low_stock_query = """
                SELECT COUNT(*) 
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE s.quantity < 10
            """
            
            params = []
            
            # Add warehouse filter if selected
            if selected_warehouse:
                value_query += " AND s.warehouse_id = %s"
                category_query += " AND s.warehouse_id = %s"
                low_stock_query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Add category filter if selected
            if selected_category:
                value_query += " AND p.category = %s"
                category_query += " AND p.category = %s"
                low_stock_query += " AND p.category = %s"
                params.append(selected_category)
            
            # Finalize category query
            category_query += " GROUP BY p.category ORDER BY total_quantity DESC"
            
            # Get total stock value
            total_value = self.db.fetch_one(value_query, params, parent_widget=self)
            if total_value and total_value[0]:
                message += f"Общая стоимость запасов: {total_value[0]:.2f} руб.\n\n"
            
            # Get stock by category
            categories = self.db.fetch_all(category_query, params, parent_widget=self)
            if categories:
                message += "Распределение по категориям:\n"
                for category, quantity in categories:
                    message += f"• {category}: {quantity} шт.\n"
                message += "\n"
            
            # Get low stock count
            low_stock_count = self.db.fetch_one(low_stock_query, params, parent_widget=self)
            if low_stock_count:
                message += f"Товаров с низким запасом: {low_stock_count[0]}\n"
            
            QMessageBox.information(self, title, message)
            
        except Exception as e:
            logging.error(f"Error generating report: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось сформировать отчет")

    def export_to_csv(self):
        """Export stock data to CSV file."""
        try:
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Base query
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Add warehouse filter if selected
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Add category filter if selected
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Add search filter if provided
            if search_text:
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Add ordering
            query += " ORDER BY p.product_name"
            
            # Define headers
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение", "Категория", "Цена за ед."]
            
            # Export data
            exporter = DataExporter(self)
            exporter.export_to_csv(query, params, headers=headers)
            
        except Exception as e:
            logging.error(f"Error exporting to CSV: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать данные в CSV")
    
    def export_to_excel(self):
        """Export stock data to Excel file."""
        try:
            selected_warehouse = self.warehouse_filter.currentData()
            selected_category = self.category_filter.currentData()
            search_text = self.search.text()
            
            # Base query
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, 
                       s.last_restocked, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                WHERE 1=1
            """
            params = []
            
            # Add warehouse filter if selected
            if selected_warehouse:
                query += " AND s.warehouse_id = %s"
                params.append(selected_warehouse)
            
            # Add category filter if selected
            if selected_category:
                query += " AND p.category = %s"
                params.append(selected_category)
            
            # Add search filter if provided
            if search_text:
                search_text = Validator.sanitize_input(search_text)
                query += " AND (p.product_name ILIKE %s OR p.category ILIKE %s)"
                params.extend([f"%{search_text}%", f"%{search_text}%"])
            
            # Add ordering
            query += " ORDER BY p.product_name"
            
            # Define headers
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение", "Категория", "Цена за ед."]
            
            # Export data
            exporter = DataExporter(self)
            exporter.export_to_excel(query, params, headers=headers, sheet_name="Запасы")
            
        except Exception as e:
            logging.error(f"Error exporting to Excel: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось экспортировать данные в Excel")
    
    def show_analysis(self):
        """Show inventory analysis dialog with visualizations."""
        try:
            dialog = InventoryAnalysisDialog(self)
            dialog.exec()
        except Exception as e:
            logging.error(f"Error showing analysis: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть анализ запасов")


class AddStockDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавить запас")
        self.setMinimumWidth(400)
        self.products = []
        self.warehouses = []
        self.load_data()
        self.setup_ui()
        
    def load_data(self):
        if not self.db:
            return
            
        try:
            # Load products
            product_query = "SELECT product_id, product_name FROM products ORDER BY product_name"
            self.products = self.db.fetch_all(product_query)
            
            # Load warehouses
            warehouse_query = "SELECT warehouse_id, warehouse_name FROM warehouses ORDER BY warehouse_name"
            self.warehouses = self.db.fetch_all(warehouse_query)
        except Exception as e:
            logging.error(f"Error loading data for stock dialog: {str(e)}")
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Добавить запас товара")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Product selection
        self.product_combo = QComboBox()
        for product_id, product_name in self.products:
            self.product_combo.addItem(product_name, product_id)
        form.addRow("Товар:", self.product_combo)
        
        # Warehouse selection
        self.warehouse_combo = QComboBox()
        for warehouse_id, warehouse_name in self.warehouses:
            self.warehouse_combo.addItem(warehouse_name, warehouse_id)
        form.addRow("Склад:", self.warehouse_combo)
        
        # Quantity
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 100000)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Количество:", self.quantity_spin)
        
        # Restock date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form.addRow("Дата поступления:", self.date_edit)
        
        layout.addLayout(form)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def accept(self):
        try:
            product_id = self.product_combo.currentData()
            warehouse_id = self.warehouse_combo.currentData()
            quantity = self.quantity_spin.value()
            restock_date = self.date_edit.date().toString("yyyy-MM-dd")
            
            # Check if this product already exists in this warehouse
            check_query = "SELECT stock_id FROM stock WHERE product_id = %s AND warehouse_id = %s"
            existing_stock = self.db.fetch_one(check_query, (product_id, warehouse_id))
            
            if existing_stock:
                # Update existing stock
                update_query = """
                    UPDATE stock 
                    SET quantity = quantity + %s,
                        last_restocked = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE product_id = %s AND warehouse_id = %s
                """
                success = self.db.execute_query(update_query, (quantity, restock_date, product_id, warehouse_id))
            else:
                # Add new stock entry
                insert_query = """
                    INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
                    VALUES (%s, %s, %s, %s)
                """
                success = self.db.execute_query(insert_query, (product_id, warehouse_id, quantity, restock_date))
                
            if success:
                super().accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить запас")
                
        except Exception as e:
            logging.error(f"Error adding stock: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить запас: {str(e)}")


class UpdateStockDialog(QDialog):
    def __init__(self, parent=None, product_name="", current_quantity=0):
        super().__init__(parent)
        self.setWindowTitle("Обновить запас")
        self.product_name = product_name
        self.current_quantity = current_quantity
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title with product name
        title = QLabel(f"Обновить запас: {self.product_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Current quantity (display only)
        current_label = QLabel(str(self.current_quantity))
        current_label.setStyleSheet("font-weight: bold;")
        form.addRow("Текущее количество:", current_label)
        
        # New quantity
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 100000)
        self.quantity_spin.setValue(self.current_quantity)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Новое количество:", self.quantity_spin)
        
        layout.addLayout(form)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def get_quantity(self):
        return self.quantity_spin.value()


class MoveStockDialog(QDialog):
    def __init__(self, parent=None, db=None, product_name="", source_warehouse="", current_quantity=0):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Переместить товар")
        self.product_name = product_name
        self.source_warehouse = source_warehouse
        self.current_quantity = current_quantity
        self.warehouses = []
        self.load_warehouses()
        self.setup_ui()
        
    def load_warehouses(self):
        if not self.db:
            return
            
        try:
            # Load warehouses except the source warehouse
            query = """
                SELECT warehouse_id, warehouse_name 
                FROM warehouses 
                WHERE warehouse_name != %s
                ORDER BY warehouse_name
            """
            self.warehouses = self.db.fetch_all(query, (self.source_warehouse,))
        except Exception as e:
            logging.error(f"Error loading warehouses for move dialog: {str(e)}")
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Переместить товар: {self.product_name}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Source warehouse (display only)
        source_label = QLabel(self.source_warehouse)
        source_label.setStyleSheet("font-weight: bold;")
        form.addRow("Исходный склад:", source_label)
        
        # Target warehouse selection
        self.target_combo = QComboBox()
        for warehouse_id, warehouse_name in self.warehouses:
            self.target_combo.addItem(warehouse_name, warehouse_id)
        form.addRow("Целевой склад:", self.target_combo)
        
        # Available quantity (display only)
        available_label = QLabel(str(self.current_quantity))
        available_label.setStyleSheet("font-weight: bold;")
        form.addRow("Доступное количество:", available_label)
        
        # Quantity to move
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, self.current_quantity)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setSingleStep(1)
        form.addRow("Количество для перемещения:", self.quantity_spin)
        
        layout.addLayout(form)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def get_move_data(self):
        return {
            "target_warehouse_id": self.target_combo.currentData(),
            "target_warehouse_name": self.target_combo.currentText(),
            "quantity": self.quantity_spin.value()
        } 