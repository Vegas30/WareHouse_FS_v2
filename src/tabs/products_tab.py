from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddProductDialog, ConfirmDialog, ExportDialog

class ProductsTab(QWidget):
    """
    Tab for managing products in the warehouse management system.
    """

    def __init__(self, db):
        """
        Initialize the products tab.

        Args:
            db: Database object for product operations
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_products()

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

        # Add a stretching element between buttons and logout
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Add elements to top panel
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_delete)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.search)
        top_panel.addItem(spacer)

        # Table for displaying products
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Цена", "Описание"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.products_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Bottom panel with additional functions
        bottom_panel = QHBoxLayout()

        # Left side of bottom panel - buttons with icons
        left_button_panel = QHBoxLayout()

        # Refresh button
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Statistics button
        self.btn_stats = QPushButton("Статистика")
        self.btn_stats.setIcon(QIcon.fromTheme("document-properties"))

        # Add buttons to left panel
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_stats)
        left_button_panel.addStretch()

        # Right side of bottom panel - export buttons
        right_button_panel = QHBoxLayout()
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Add elements to right panel
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Assemble bottom panel from left and right parts
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Assemble main interface
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.products_table)
        main_layout.addLayout(bottom_panel)

        self.setLayout(main_layout)

        # Connect event handlers
        self.btn_add.clicked.connect(self.add_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_edit.clicked.connect(self.edit_product)
        self.btn_refresh.clicked.connect(self.load_products)
        self.btn_stats.clicked.connect(self.show_stats)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_products(self):
        """Load products from database and display in table."""
        try:
            query = "SELECT product_id, product_name, category, unit_price, product_description FROM products ORDER BY product_name"
            products = self.db.fetch_all(query)

            self.products_table.setRowCount(len(products))

            for row_idx, product in enumerate(products):
                for col_idx, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.products_table.setItem(row_idx, col_idx, item)
        except Exception as e:
            logging.error(f"Error loading products: {str(e)}")
            QMessageBox.critical(self, "Error", "Failed to load products data")

    def handle_search(self):
        """Handle product search by typed text."""
        try:
            search_text = self.search.text()

            query = """
                SELECT product_id, product_name, category, unit_price, product_description 
                FROM products 
                WHERE product_name ILIKE %s 
                   OR category ILIKE %s 
                   OR product_description ILIKE %s
                ORDER BY product_name
            """
            products = self.db.fetch_all(query, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))

            self.products_table.setRowCount(len(products))

            for row_idx, product in enumerate(products):
                for col_idx, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.products_table.setItem(row_idx, col_idx, item)
        except Exception as e:
            logging.error(f"Error searching products: {str(e)}")

    def add_product(self):
        """Show dialog to add a new product."""
        dialog = AddProductDialog(self, self.db)
        if dialog.exec():
            product_data = dialog.get_product_data()
            try:
                query = """
                    INSERT INTO products (product_name, product_description, category, unit_price)
                    VALUES (%s, %s, %s, %s)
                """
                params = (
                    product_data["name"],
                    product_data["description"],
                    product_data["category"],
                    product_data["price"]
                )
                success = self.db.execute_query(query, params)
                if success:
                    self.load_products()
                    QMessageBox.information(self, "Успех", "Товар успешно добавлен")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить товар")
            except Exception as e:
                logging.error(f"Error adding product: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар: {str(e)}")

    def delete_product(self):
        """Delete selected product."""
        selected_rows = self.products_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления")
            return

        row = selected_rows[0].row()
        product_id = self.products_table.item(row, 0).text()
        product_name = self.products_table.item(row, 1).text()

        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить товар:\n{product_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                query = "DELETE FROM products WHERE product_id = %s"
                success = self.db.execute_query(query, (product_id,))
                if success:
                    self.load_products()
                    QMessageBox.information(self, "Успех", "Товар успешно удален")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить товар")
            except Exception as e:
                logging.error(f"Error deleting product: {str(e)}")
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")

    def edit_product(self):
        """Edit selected product."""
        selected_rows = self.products_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите товар для редактирования")
            return

        row = selected_rows[0].row()
        product_id = self.products_table.item(row, 0).text()

        try:
            query = "SELECT product_name, product_description, category, unit_price FROM products WHERE product_id = %s"
            product = self.db.fetch_one(query, (product_id,))
            
            if product:
                dialog = AddProductDialog(self, self.db)
                dialog.setWindowTitle("Редактировать товар")
                
                # Fill dialog with current product data
                dialog.name_input.setText(product[0])
                dialog.description_input.setText(product[1])
                index = dialog.category_input.findText(product[2])
                if index >= 0:
                    dialog.category_input.setCurrentIndex(index)
                dialog.price_input.setValue(float(product[3]))

                if dialog.exec():
                    updated_data = dialog.get_product_data()
                    update_query = """
                        UPDATE products 
                        SET product_name = %s, 
                            product_description = %s, 
                            category = %s, 
                            unit_price = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE product_id = %s
                    """
                    update_params = (
                        updated_data["name"],
                        updated_data["description"],
                        updated_data["category"],
                        updated_data["price"],
                        product_id
                    )
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        self.load_products()
                        QMessageBox.information(self, "Успех", "Товар успешно обновлен")
                    else:
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить товар")
        except Exception as e:
            logging.error(f"Error editing product: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать товар: {str(e)}")

    def export_data(self):
        """Export products data."""
        dialog = ExportDialog(self, "Экспорт товаров")
        if dialog.exec():
            export_data = dialog.get_export_data()
            file_path = export_data["file_path"]
            
            if not file_path:
                QMessageBox.warning(self, "Внимание", "Выберите путь для сохранения файла")
                return
            
            # Here would be the actual export implementation
            # This is just a placeholder message
            QMessageBox.information(self, "Экспорт", f"Данные успешно экспортированы в {file_path}")

    def show_stats(self):
        """Show statistics about products."""
        QMessageBox.information(self, "Статистика", "Функция статистики пока не реализована")