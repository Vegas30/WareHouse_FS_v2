from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QDateEdit, QSpinBox,
                             QDoubleSpinBox, QGridLayout, QFormLayout, QTextEdit, QDialogButtonBox,
                             QFileDialog)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import logging
from database import Database

class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle("Добавление товара" if not product else "Редактирование товара")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Название товара
        self.name_edit = QLineEdit()
        if self.product:
            self.name_edit.setText(self.product[1])  # product_name
        form.addRow("Название:", self.name_edit)
        
        # Описание товара
        self.description_edit = QTextEdit()
        if self.product and self.product[2]:  # product_description
            self.description_edit.setText(self.product[2])
        form.addRow("Описание:", self.description_edit)
        
        # Категория
        self.category_combo = QComboBox()
        categories = ['электроника', 'одежда', 'обувь', 'мебель', 'товары для спорта', 
                     'инструменты', 'бытовая техника', 'здоровье', 'товары для дома', 'продукты']
        self.category_combo.addItems(categories)
        if self.product and self.product[3]:  # category
            self.category_combo.setCurrentText(self.product[3])
        form.addRow("Категория:", self.category_combo)
        
        # Цена
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.01, 1000000)
        self.price_spin.setSingleStep(1)
        self.price_spin.setPrefix("₽ ")
        if self.product:
            self.price_spin.setValue(float(self.product[4]))  # unit_price
        form.addRow("Цена:", self.price_spin)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
    def get_product_data(self):
        return {
            "name": self.name_edit.text(),
            "description": self.description_edit.toPlainText(),
            "category": self.category_combo.currentText(),
            "price": self.price_spin.value()
        }

class SupplierDialog(QDialog):
    def __init__(self, parent=None, supplier=None):
        super().__init__(parent)
        self.supplier = supplier
        self.setWindowTitle("Добавление поставщика" if not supplier else "Редактирование поставщика")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Название поставщика
        self.name_edit = QLineEdit()
        if self.supplier:
            self.name_edit.setText(self.supplier[1])  # supplier_name
        form.addRow("Название:", self.name_edit)
        
        # Контактное лицо
        self.contact_edit = QLineEdit()
        if self.supplier and self.supplier[2]:  # contact_person
            self.contact_edit.setText(self.supplier[2])
        form.addRow("Контактное лицо:", self.contact_edit)
        
        # Телефон
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("89991234567")
        if self.supplier and self.supplier[3]:  # phone_number
            self.phone_edit.setText(self.supplier[3])
        form.addRow("Телефон:", self.phone_edit)
        
        # Email
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("email@example.com")
        if self.supplier and self.supplier[4]:  # email
            self.email_edit.setText(self.supplier[4])
        form.addRow("Email:", self.email_edit)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
    def get_supplier_data(self):
        return {
            "name": self.name_edit.text(),
            "contact": self.contact_edit.text(),
            "phone": self.phone_edit.text(),
            "email": self.email_edit.text()
        }

class WarehouseDialog(QDialog):
    def __init__(self, parent=None, warehouse=None):
        super().__init__(parent)
        self.warehouse = warehouse
        self.setWindowTitle("Добавление склада" if not warehouse else "Редактирование склада")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Название склада
        self.name_edit = QLineEdit()
        if self.warehouse:
            self.name_edit.setText(self.warehouse[1])  # warehouse_name
        form.addRow("Название:", self.name_edit)
        
        # Местоположение
        self.location_edit = QLineEdit()
        if self.warehouse:
            self.location_edit.setText(self.warehouse[2])  # location
        form.addRow("Местоположение:", self.location_edit)
        
        # Вместимость
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setRange(1, 1000000)
        self.capacity_spin.setSingleStep(10)
        if self.warehouse:
            self.capacity_spin.setValue(self.warehouse[3])  # capacity
        form.addRow("Вместимость:", self.capacity_spin)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
    def get_warehouse_data(self):
        return {
            "name": self.name_edit.text(),
            "location": self.location_edit.text(),
            "capacity": self.capacity_spin.value()
        }

class OrderDialog(QDialog):
    def __init__(self, parent=None, order=None, suppliers=None):
        super().__init__(parent)
        self.order = order
        self.suppliers = suppliers or []
        self.setWindowTitle("Добавление заказа" if not order else "Редактирование заказа")
        self.setMinimumWidth(450)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Дата заказа
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        if self.order:
            order_date = QDate.fromString(str(self.order[1]), "yyyy-MM-dd")  # order_date
            self.date_edit.setDate(order_date)
        form.addRow("Дата заказа:", self.date_edit)
        
        # Поставщик
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItem("-- Выберите поставщика --", None)
        
        for supplier in self.suppliers:
            self.supplier_combo.addItem(supplier[1], supplier[0])  # supplier_name, supplier_id
            
        if self.order and self.order[2]:  # supplier_id
            for i in range(self.supplier_combo.count()):
                if self.supplier_combo.itemData(i) == self.order[2]:
                    self.supplier_combo.setCurrentIndex(i)
                    break
                    
        form.addRow("Поставщик:", self.supplier_combo)
        
        # Статус
        self.status_combo = QComboBox()
        statuses = ['в обработке', 'доставлен', 'отменен']
        self.status_combo.addItems(statuses)
        if self.order and self.order[4]:  # status
            self.status_combo.setCurrentText(self.order[4])
        form.addRow("Статус:", self.status_combo)
        
        # Сумма заказа (только для редактирования)
        self.total_spin = QDoubleSpinBox()
        self.total_spin.setRange(0.01, 10000000)
        self.total_spin.setSingleStep(100)
        self.total_spin.setPrefix("₽ ")
        if self.order:
            self.total_spin.setValue(float(self.order[3]))  # total_amount
        form.addRow("Сумма заказа:", self.total_spin)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
    def get_order_data(self):
        return {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "supplier_id": self.supplier_combo.currentData(),
            "status": self.status_combo.currentText(),
            "total_amount": self.total_spin.value()
        }

class StockDialog(QDialog):
    def __init__(self, parent=None, stock=None, products=None, warehouses=None):
        super().__init__(parent)
        self.stock = stock
        self.products = products or []
        self.warehouses = warehouses or []
        self.setWindowTitle("Добавление запаса" if not stock else "Редактирование запаса")
        self.setMinimumWidth(450)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Товар
        self.product_combo = QComboBox()
        self.product_combo.addItem("-- Выберите товар --", None)
        
        for product in self.products:
            self.product_combo.addItem(product[1], product[0])  # product_name, product_id
            
        if self.stock and self.stock[1]:  # product_id
            for i in range(self.product_combo.count()):
                if self.product_combo.itemData(i) == self.stock[1]:
                    self.product_combo.setCurrentIndex(i)
                    break
                    
        form.addRow("Товар:", self.product_combo)
        
        # Склад
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.addItem("-- Выберите склад --", None)
        
        for warehouse in self.warehouses:
            self.warehouse_combo.addItem(warehouse[1], warehouse[0])  # warehouse_name, warehouse_id
            
        if self.stock and self.stock[2]:  # warehouse_id
            for i in range(self.warehouse_combo.count()):
                if self.warehouse_combo.itemData(i) == self.stock[2]:
                    self.warehouse_combo.setCurrentIndex(i)
                    break
                    
        form.addRow("Склад:", self.warehouse_combo)
        
        # Количество
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 100000)
        self.quantity_spin.setSingleStep(1)
        if self.stock:
            self.quantity_spin.setValue(self.stock[3])  # quantity
        form.addRow("Количество:", self.quantity_spin)
        
        # Дата последнего пополнения
        self.restock_date = QDateEdit()
        self.restock_date.setCalendarPopup(True)
        self.restock_date.setDate(QDate.currentDate())
        if self.stock and self.stock[4]:  # last_restocked
            restock_date = QDate.fromString(str(self.stock[4]), "yyyy-MM-dd")
            self.restock_date.setDate(restock_date)
        form.addRow("Дата пополнения:", self.restock_date)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
        
    def get_stock_data(self):
        return {
            "product_id": self.product_combo.currentData(),
            "warehouse_id": self.warehouse_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "restock_date": self.restock_date.date().toString("yyyy-MM-dd")
        }

class AddProductDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавить товар")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Новый товар")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Product name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        form.addRow("Название:", self.name_input)
        
        # Product description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Введите описание товара")
        self.description_input.setMaximumHeight(100)
        form.addRow("Описание:", self.description_input)
        
        # Category selection
        self.category_input = QComboBox()
        categories = ["электроника", "одежда", "обувь", "мебель", 
                      "товары для спорта", "инструменты", "бытовая техника", 
                      "здоровье", "товары для дома", "продукты"]
        self.category_input.addItems(categories)
        form.addRow("Категория:", self.category_input)
        
        # Price
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 1000000.00)
        self.price_input.setValue(0.01)
        self.price_input.setSingleStep(1.00)
        self.price_input.setPrefix("₽ ")
        form.addRow("Цена:", self.price_input)
        
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
    
    def get_product_data(self):
        return {
            "name": self.name_input.text(),
            "description": self.description_input.toPlainText(),
            "category": self.category_input.currentText(),
            "price": self.price_input.value()
        }

class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавить поставщика")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Новый поставщик")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Supplier name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название компании")
        form.addRow("Название:", self.name_input)
        
        # Contact person
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Введите контактное лицо")
        form.addRow("Контактное лицо:", self.contact_input)
        
        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Введите номер телефона (11 цифр)")
        self.phone_input.setInputMask("99999999999")
        form.addRow("Телефон:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите email")
        form.addRow("Email:", self.email_input)
        
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
    
    def get_supplier_data(self):
        return {
            "name": self.name_input.text(),
            "contact": self.contact_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }

class AddOrderDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Создать заказ")
        self.setMinimumWidth(450)
        self.suppliers = []
        self.load_suppliers()
        self.setup_ui()
        
    def load_suppliers(self):
        if self.db:
            try:
                query = "SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name"
                self.suppliers = self.db.fetch_all(query)
            except Exception as e:
                logging.error(f"Error loading suppliers: {str(e)}")
                self.suppliers = []
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Новый заказ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Order date
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        form.addRow("Дата заказа:", self.date_input)
        
        # Supplier selection
        self.supplier_input = QComboBox()
        for supplier_id, supplier_name in self.suppliers:
            self.supplier_input.addItem(supplier_name, supplier_id)
        form.addRow("Поставщик:", self.supplier_input)
        
        # Total amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 10000000.00)
        self.amount_input.setValue(0.01)
        self.amount_input.setSingleStep(100.00)
        self.amount_input.setPrefix("₽ ")
        form.addRow("Сумма заказа:", self.amount_input)
        
        # Status
        self.status_input = QComboBox()
        statuses = ["в обработке", "доставлен", "отменен"]
        self.status_input.addItems(statuses)
        form.addRow("Статус:", self.status_input)
        
        # Note 
        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Введите примечание к заказу (необязательно)")
        self.note_input.setMaximumHeight(80)
        form.addRow("Примечание:", self.note_input)
        
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
    
    def get_order_data(self):
        return {
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "supplier_id": self.supplier_input.currentData(),
            "amount": self.amount_input.value(),
            "status": self.status_input.currentText(),
            "note": self.note_input.toPlainText()
        }

class AddWarehouseDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Добавить склад")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Новый склад")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # Warehouse name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название склада")
        form.addRow("Название:", self.name_input)
        
        # Location
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Введите местоположение")
        form.addRow("Адрес:", self.location_input)
        
        # Capacity
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 1000000)
        self.capacity_input.setValue(1000)
        self.capacity_input.setSingleStep(100)
        form.addRow("Вместимость:", self.capacity_input)
        
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
    
    def get_warehouse_data(self):
        return {
            "name": self.name_input.text(),
            "location": self.location_input.text(),
            "capacity": self.capacity_input.value()
        }

class ConfirmDialog(QDialog):
    def __init__(self, parent=None, title="Подтверждение", message="Вы уверены?"):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        layout = QVBoxLayout()
        
        # Message
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # Buttons
        button_box = QHBoxLayout()
        
        yes_button = QPushButton("Да")
        yes_button.clicked.connect(self.accept)
        
        no_button = QPushButton("Нет")
        no_button.clicked.connect(self.reject)
        
        button_box.addWidget(yes_button)
        button_box.addWidget(no_button)
        
        layout.addLayout(button_box)
        self.setLayout(layout)

class ExportDialog(QDialog):
    def __init__(self, parent=None, title="Экспорт данных"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.file_path = ""
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Экспорт данных")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Выберите путь для сохранения...")
        
        browse_button = QPushButton("Обзор...")
        browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        
        layout.addLayout(file_layout)
        
        # Export format 
        format_layout = QHBoxLayout()
        format_label = QLabel("Формат экспорта:")
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Excel (.xlsx)", "CSV (.csv)", "PDF (.pdf)"])
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        
        layout.addLayout(format_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def browse_file(self):
        formats = {
            0: "Excel Files (*.xlsx)",
            1: "CSV Files (*.csv)",
            2: "PDF Files (*.pdf)"
        }
        current_format = self.format_combo.currentIndex()
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить файл",
            "",
            formats[current_format]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_input.setText(file_path)
    
    def get_export_data(self):
        return {
            "file_path": self.file_path,
            "format": self.format_combo.currentText()
        }

class EmailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Отправить Email")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Отправка Email")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Form layout
        form = QFormLayout()
        
        # To field
        self.to_input = QLineEdit()
        self.to_input.setPlaceholderText("Введите email получателя")
        form.addRow("Кому:", self.to_input)
        
        # Subject
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Введите тему письма")
        form.addRow("Тема:", self.subject_input)
        
        # Message
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Введите текст сообщения")
        form.addRow("Сообщение:", self.message_input)
        
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
    
    def get_email_data(self):
        return {
            "to": self.to_input.text(),
            "subject": self.subject_input.text(),
            "message": self.message_input.toPlainText()
        } 