# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QDateEdit, QSpinBox,
                             QDoubleSpinBox, QGridLayout, QFormLayout, QTextEdit, QDialogButtonBox,
                             QFileDialog, QTableWidget, QAbstractItemView, QTableWidgetItem)
# Импорт базовых классов и типов данных из PyQt6
from PyQt6.QtCore import Qt, QDate
# Импорт шрифтов из PyQt6
from PyQt6.QtGui import QFont
# Импорт модуля логирования
import logging
# Импорт модуля базы данных
from database import Database
# Импорт модуля для работы с датами
import datetime

# Base Dialog Class (optional, for common features like button boxes)
class BaseDialog(QDialog):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def add_row(self, label, widget):
        self.form_layout.addRow(label, widget)

# Класс диалогового окна для работы с товарами
class ProductDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, product=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение переданного товара
        self.product = product
        # Установка заголовка окна в зависимости от режима (добавление/редактирование)
        self.setWindowTitle("Добавление товара" if not product else "Редактирование товара")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета для окна
        layout = QVBoxLayout(self)
        
        # Создание макета формы для полей ввода
        form = QFormLayout()
        
        # Создание поля для ввода названия товара
        self.name_edit = QLineEdit()
        # Если товар передан (режим редактирования), заполняем поле его названием
        if self.product:
            self.name_edit.setText(self.product[1])  # product_name
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_edit)
        
        # Создание поля для ввода описания товара
        self.description_edit = QTextEdit()
        # Если товар передан и у него есть описание, заполняем поле
        if self.product and self.product[2]:  # product_description
            self.description_edit.setText(self.product[2])
        # Добавление поля в форму с меткой
        form.addRow("Описание:", self.description_edit)
        
        # Создание выпадающего списка для выбора категории
        self.category_combo = QComboBox()
        # Список доступных категорий товаров
        categories = ['электроника', 'одежда', 'обувь', 'мебель', 'товары для спорта', 
                     'инструменты', 'бытовая техника', 'здоровье', 'товары для дома', 'продукты']
        # Добавление категорий в выпадающий список
        self.category_combo.addItems(categories)
        # Если товар передан, устанавливаем текущую категорию
        if self.product and self.product[3]:  # category
            self.category_combo.setCurrentText(self.product[3])
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Категория:", self.category_combo)
        
        # Создание поля для ввода цены с возможностью выбора числа
        self.price_spin = QDoubleSpinBox()
        # Установка диапазона цен
        self.price_spin.setRange(0.01, 1000000)
        # Установка шага изменения цены
        self.price_spin.setSingleStep(1)
        # Добавление символа валюты
        self.price_spin.setPrefix("₽ ")
        # Если товар передан, устанавливаем его цену
        if self.product:
            self.price_spin.setValue(float(self.product[4]))  # unit_price
        # Добавление поля в форму с меткой
        form.addRow("Цена:", self.price_spin)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание макета для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создание кнопки "Сохранить"
        save_button = QPushButton("Сохранить")
        # Подключение сигнала нажатия к кнопке
        save_button.clicked.connect(self.accept)
        
        # Создание кнопки "Отмена"
        cancel_button = QPushButton("Отмена")
        # Подключение сигнала нажатия к кнопке
        cancel_button.clicked.connect(self.reject)
        # Установка стиля для кнопки отмены
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        # Добавление кнопок в макет
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(buttons_layout)
        
    # Метод для получения данных о товаре
    def get_product_data(self):
        # Возврат словаря с данными товара
        return {
            "name": self.name_edit.text(),
            "description": self.description_edit.toPlainText(),
            "category": self.category_combo.currentText(),
            "price": self.price_spin.value()
        }

# Класс диалогового окна для работы с поставщиками
class SupplierDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, supplier=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение переданного поставщика
        self.supplier = supplier
        # Установка заголовка окна в зависимости от режима (добавление/редактирование)
        self.setWindowTitle("Добавление поставщика" if not supplier else "Редактирование поставщика")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета для окна
        layout = QVBoxLayout(self)
        
        # Создание макета формы для полей ввода
        form = QFormLayout()
        
        # Создание поля для ввода названия поставщика
        self.name_edit = QLineEdit()
        # Если поставщик передан (режим редактирования), заполняем поле его названием
        if self.supplier:
            self.name_edit.setText(self.supplier[1])  # supplier_name
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_edit)
        
        # Создание поля для ввода контактного лица
        self.contact_edit = QLineEdit()
        # Если поставщик передан и указано контактное лицо, заполняем поле
        if self.supplier and self.supplier[2]:  # contact_person
            self.contact_edit.setText(self.supplier[2])
        # Добавление поля в форму с меткой
        form.addRow("Контактное лицо:", self.contact_edit)
        
        # Создание поля для ввода телефона
        self.phone_edit = QLineEdit()
        # Установка подсказки для формата номера телефона
        self.phone_edit.setPlaceholderText("89991234567")
        # Если поставщик передан и указан телефон, заполняем поле
        if self.supplier and self.supplier[3]:  # phone_number
            self.phone_edit.setText(self.supplier[3])
        # Добавление поля в форму с меткой
        form.addRow("Телефон:", self.phone_edit)
        
        # Создание поля для ввода email
        self.email_edit = QLineEdit()
        # Установка подсказки для формата email
        self.email_edit.setPlaceholderText("email@example.com")
        # Если поставщик передан и указан email, заполняем поле
        if self.supplier and self.supplier[4]:  # email
            self.email_edit.setText(self.supplier[4])
        # Добавление поля в форму с меткой
        form.addRow("Email:", self.email_edit)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание макета для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создание кнопки "Сохранить"
        save_button = QPushButton("Сохранить")
        # Подключение сигнала нажатия к кнопке
        save_button.clicked.connect(self.accept)
        
        # Создание кнопки "Отмена"
        cancel_button = QPushButton("Отмена")
        # Подключение сигнала нажатия к кнопке
        cancel_button.clicked.connect(self.reject)
        # Установка стиля для кнопки отмены
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        # Добавление кнопок в макет
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(buttons_layout)
        
    # Метод для получения данных о поставщике
    def get_supplier_data(self):
        # Возврат словаря с данными поставщика
        return {
            "name": self.name_edit.text(),
            "contact": self.contact_edit.text(),
            "phone": self.phone_edit.text(),
            "email": self.email_edit.text()
        }

# Класс диалогового окна для работы со складами
class WarehouseDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, warehouse=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение переданного склада
        self.warehouse = warehouse
        # Установка заголовка окна в зависимости от режима (добавление/редактирование)
        self.setWindowTitle("Добавление склада" if not warehouse else "Редактирование склада")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета для окна
        layout = QVBoxLayout(self)
        
        # Создание макета формы для полей ввода
        form = QFormLayout()
        
        # Создание поля для ввода названия склада
        self.name_edit = QLineEdit()
        # Если склад передан (режим редактирования), заполняем поле его названием
        if self.warehouse:
            self.name_edit.setText(self.warehouse[1])  # warehouse_name
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_edit)
        
        # Создание поля для ввода местоположения
        self.location_edit = QLineEdit()
        # Если склад передан, заполняем поле его местоположением
        if self.warehouse:
            self.location_edit.setText(self.warehouse[2])  # location
        # Добавление поля в форму с меткой
        form.addRow("Местоположение:", self.location_edit)
        
        # Создание поля для ввода вместимости
        self.capacity_spin = QSpinBox()
        # Установка диапазона значений вместимости
        self.capacity_spin.setRange(1, 1000000)
        # Установка шага изменения значения
        self.capacity_spin.setSingleStep(10)
        # Если склад передан, устанавливаем его вместимость
        if self.warehouse:
            self.capacity_spin.setValue(self.warehouse[3])  # capacity
        # Добавление поля в форму с меткой
        form.addRow("Вместимость:", self.capacity_spin)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание макета для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создание кнопки "Сохранить"
        save_button = QPushButton("Сохранить")
        # Подключение сигнала нажатия к кнопке
        save_button.clicked.connect(self.accept)
        
        # Создание кнопки "Отмена"
        cancel_button = QPushButton("Отмена")
        # Подключение сигнала нажатия к кнопке
        cancel_button.clicked.connect(self.reject)
        # Установка стиля для кнопки отмены
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        # Добавление кнопок в макет
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(buttons_layout)
        
    # Метод для получения данных о складе
    def get_warehouse_data(self):
        # Возврат словаря с данными склада
        return {
            "name": self.name_edit.text(),
            "location": self.location_edit.text(),
            "capacity": self.capacity_spin.value()
        }

# Класс диалогового окна для работы с заказами
class OrderDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, order=None, suppliers=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение переданного заказа
        self.order = order
        # Сохранение списка поставщиков
        self.suppliers = suppliers or []
        # Установка заголовка окна в зависимости от режима (добавление/редактирование)
        self.setWindowTitle("Добавление заказа" if not order else "Редактирование заказа")
        # Установка минимальной ширины окна
        self.setMinimumWidth(450)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета для окна
        layout = QVBoxLayout(self)
        
        # Создание макета формы для полей ввода
        form = QFormLayout()
        
        # Создание поля для выбора даты заказа
        self.date_edit = QDateEdit()
        # Включение всплывающего календаря
        self.date_edit.setCalendarPopup(True)
        # Установка текущей даты по умолчанию
        self.date_edit.setDate(QDate.currentDate())
        # Если заказ передан, устанавливаем его дату
        if self.order:
            order_date = QDate.fromString(str(self.order[1]), "yyyy-MM-dd")  # order_date
            self.date_edit.setDate(order_date)
        # Добавление поля в форму с меткой
        form.addRow("Дата заказа:", self.date_edit)
        
        # Создание выпадающего списка для выбора поставщика
        self.supplier_combo = QComboBox()
        # Добавление пустого элемента в начало списка
        self.supplier_combo.addItem("-- Выберите поставщика --", None)
        
        # Добавление поставщиков в выпадающий список
        for supplier in self.suppliers:
            self.supplier_combo.addItem(supplier[1], supplier[0])  # supplier_name, supplier_id
            
        # Если заказ передан, устанавливаем текущего поставщика
        if self.order and self.order[2]:  # supplier_id
            for i in range(self.supplier_combo.count()):
                if self.supplier_combo.itemData(i) == self.order[2]:
                    self.supplier_combo.setCurrentIndex(i)
                    break
                    
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Поставщик:", self.supplier_combo)
        
        # Создание выпадающего списка для выбора статуса
        self.status_combo = QComboBox()
        # Список возможных статусов заказа
        statuses = ['в обработке', 'доставлен', 'отменен']
        # Добавление статусов в выпадающий список
        self.status_combo.addItems(statuses)
        # Если заказ передан, устанавливаем его статус
        if self.order and self.order[4]:  # status
            self.status_combo.setCurrentText(self.order[4])
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Статус:", self.status_combo)
        
        # Создание поля для ввода суммы заказа
        self.total_spin = QDoubleSpinBox()
        # Установка диапазона значений суммы
        self.total_spin.setRange(0.01, 10000000)
        # Установка шага изменения значения
        self.total_spin.setSingleStep(100)
        # Добавление символа валюты
        self.total_spin.setPrefix("₽ ")
        # Если заказ передан, устанавливаем его сумму
        if self.order:
            self.total_spin.setValue(float(self.order[3]))  # total_amount
        # Добавление поля в форму с меткой
        form.addRow("Сумма заказа:", self.total_spin)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание макета для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создание кнопки "Сохранить"
        save_button = QPushButton("Сохранить")
        # Подключение сигнала нажатия к кнопке
        save_button.clicked.connect(self.accept)
        
        # Создание кнопки "Отмена"
        cancel_button = QPushButton("Отмена")
        # Подключение сигнала нажатия к кнопке
        cancel_button.clicked.connect(self.reject)
        # Установка стиля для кнопки отмены
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        # Добавление кнопок в макет
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(buttons_layout)
        
    # Метод для получения данных о заказе
    def get_order_data(self):
        # Возврат словаря с данными заказа
        return {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "supplier_id": self.supplier_combo.currentData(),
            "status": self.status_combo.currentText(),
            "total_amount": self.total_spin.value()
        }

# Класс диалогового окна для работы с запасами
class StockDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, stock=None, products=None, warehouses=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение переданного запаса
        self.stock = stock
        # Сохранение списка товаров
        self.products = products or []
        # Сохранение списка складов
        self.warehouses = warehouses or []
        # Установка заголовка окна в зависимости от режима (добавление/редактирование)
        self.setWindowTitle("Добавление запаса" if not stock else "Редактирование запаса")
        # Установка минимальной ширины окна
        self.setMinimumWidth(450)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета для окна
        layout = QVBoxLayout(self)
        
        # Создание макета формы для полей ввода
        form = QFormLayout()
        
        # Создание выпадающего списка для выбора товара
        self.product_combo = QComboBox()
        # Добавление пустого элемента в начало списка
        self.product_combo.addItem("-- Выберите товар --", None)
        
        # Добавление товаров в выпадающий список
        for product in self.products:
            self.product_combo.addItem(product[1], product[0])  # product_name, product_id
            
        # Если запас передан, устанавливаем текущий товар
        if self.stock and self.stock[1]:  # product_id
            for i in range(self.product_combo.count()):
                if self.product_combo.itemData(i) == self.stock[1]:
                    self.product_combo.setCurrentIndex(i)
                    break
                    
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Товар:", self.product_combo)
        
        # Создание выпадающего списка для выбора склада
        self.warehouse_combo = QComboBox()
        # Добавление пустого элемента в начало списка
        self.warehouse_combo.addItem("-- Выберите склад --", None)
        
        # Добавление складов в выпадающий список
        for warehouse in self.warehouses:
            self.warehouse_combo.addItem(warehouse[1], warehouse[0])  # warehouse_name, warehouse_id
            
        # Если запас передан, устанавливаем текущий склад
        if self.stock and self.stock[2]:  # warehouse_id
            for i in range(self.warehouse_combo.count()):
                if self.warehouse_combo.itemData(i) == self.stock[2]:
                    self.warehouse_combo.setCurrentIndex(i)
                    break
                    
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Склад:", self.warehouse_combo)
        
        # Создание поля для ввода количества
        self.quantity_spin = QSpinBox()
        # Установка диапазона значений количества
        self.quantity_spin.setRange(0, 100000)
        # Установка шага изменения значения
        self.quantity_spin.setSingleStep(1)
        # Если запас передан, устанавливаем его количество
        if self.stock:
            self.quantity_spin.setValue(self.stock[3])  # quantity
        # Добавление поля в форму с меткой
        form.addRow("Количество:", self.quantity_spin)
        
        # Создание поля для выбора даты последнего пополнения
        self.restock_date = QDateEdit()
        # Включение всплывающего календаря
        self.restock_date.setCalendarPopup(True)
        # Установка текущей даты по умолчанию
        self.restock_date.setDate(QDate.currentDate())
        # Если запас передан, устанавливаем дату последнего пополнения
        if self.stock and self.stock[4]:  # last_restocked
            restock_date = QDate.fromString(str(self.stock[4]), "yyyy-MM-dd")
            self.restock_date.setDate(restock_date)
        # Добавление поля в форму с меткой
        form.addRow("Дата пополнения:", self.restock_date)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание макета для кнопок
        buttons_layout = QHBoxLayout()
        
        # Создание кнопки "Сохранить"
        save_button = QPushButton("Сохранить")
        # Подключение сигнала нажатия к кнопке
        save_button.clicked.connect(self.accept)
        
        # Создание кнопки "Отмена"
        cancel_button = QPushButton("Отмена")
        # Подключение сигнала нажатия к кнопке
        cancel_button.clicked.connect(self.reject)
        # Установка стиля для кнопки отмены
        cancel_button.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
        # Добавление кнопок в макет
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(buttons_layout)
        
    # Метод для получения данных о запасе
    def get_stock_data(self):
        # Возврат словаря с данными запаса
        return {
            "product_id": self.product_combo.currentData(),
            "warehouse_id": self.warehouse_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "restock_date": self.restock_date.date().toString("yyyy-MM-dd")
        }

# Класс диалогового окна для добавления товара
class AddProductDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, db=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Добавить товар")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Новый товар")
        # Выравнивание заголовка по центру
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка шрифта для заголовка
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Установка стиля для заголовка
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        # Добавление заголовка в макет
        layout.addWidget(title)
        
        # Создание макета формы
        form = QFormLayout()
        
        # Создание поля для ввода названия товара
        self.name_input = QLineEdit()
        # Установка подсказки для поля
        self.name_input.setPlaceholderText("Введите название товара")
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_input)
        
        # Создание поля для ввода описания товара
        self.description_input = QTextEdit()
        # Установка подсказки для поля
        self.description_input.setPlaceholderText("Введите описание товара")
        # Установка максимальной высоты поля
        self.description_input.setMaximumHeight(100)
        # Добавление поля в форму с меткой
        form.addRow("Описание:", self.description_input)
        
        # Создание выпадающего списка для выбора категории
        self.category_input = QComboBox()
        # Список доступных категорий
        categories = ["электроника", "одежда", "обувь", "мебель", 
                      "товары для спорта", "инструменты", "бытовая техника", 
                      "здоровье", "товары для дома", "продукты"]
        # Добавление категорий в выпадающий список
        self.category_input.addItems(categories)
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Категория:", self.category_input)
        
        # Создание поля для ввода цены
        self.price_input = QDoubleSpinBox()
        # Установка диапазона цен
        self.price_input.setRange(0.01, 1000000.00)
        # Установка значения по умолчанию
        self.price_input.setValue(0.01)
        # Установка шага изменения цены
        self.price_input.setSingleStep(1.00)
        # Добавление символа валюты
        self.price_input.setPrefix("₽ ")
        # Добавление поля в форму с меткой
        form.addRow("Цена:", self.price_input)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание панели кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Подключение сигналов к кнопкам
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление панели кнопок в макет
        layout.addWidget(button_box)
        # Установка макета для окна
        self.setLayout(layout)
    
    # Метод для получения данных о товаре
    def get_product_data(self):
        # Возврат словаря с данными товара
        return {
            "name": self.name_input.text(),
            "description": self.description_input.toPlainText(),
            "category": self.category_input.currentText(),
            "price": self.price_input.value()
        }

# Класс диалогового окна для добавления поставщика
class AddSupplierDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, db=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Добавить поставщика")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Новый поставщик")
        # Выравнивание заголовка по центру
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка шрифта для заголовка
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Установка стиля для заголовка
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        # Добавление заголовка в макет
        layout.addWidget(title)
        
        # Создание макета формы
        form = QFormLayout()
        
        # Создание поля для ввода названия поставщика
        self.name_input = QLineEdit()
        # Установка подсказки для поля
        self.name_input.setPlaceholderText("Введите название компании")
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_input)
        
        # Создание поля для ввода контактного лица
        self.contact_input = QLineEdit()
        # Установка подсказки для поля
        self.contact_input.setPlaceholderText("Введите контактное лицо")
        # Добавление поля в форму с меткой
        form.addRow("Контактное лицо:", self.contact_input)
        
        # Создание поля для ввода телефона
        self.phone_input = QLineEdit()
        # Установка подсказки для поля
        self.phone_input.setPlaceholderText("Введите номер телефона (11 цифр)")
        # Установка маски ввода для телефона
        self.phone_input.setInputMask("99999999999")
        # Добавление поля в форму с меткой
        form.addRow("Телефон:", self.phone_input)
        
        # Создание поля для ввода email
        self.email_input = QLineEdit()
        # Установка подсказки для поля
        self.email_input.setPlaceholderText("Введите email")
        # Добавление поля в форму с меткой
        form.addRow("Email:", self.email_input)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание панели кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Подключение сигналов к кнопкам
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление панели кнопок в макет
        layout.addWidget(button_box)
        # Установка макета для окна
        self.setLayout(layout)
    
    # Метод для получения данных о поставщике
    def get_supplier_data(self):
        # Возврат словаря с данными поставщика
        return {
            "name": self.name_input.text(),
            "contact": self.contact_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }

# Класс диалогового окна для добавления заказа
class AddOrderDialog(BaseDialog):
    """Диалог для создания и редактирования заказов поставщиков."""
    def __init__(self, parent=None, db=None):
        super().__init__("Создать заказ", parent)
        self.db = db
        self.setMinimumSize(600, 500)

        # --- Top Section: Supplier and Product Selection ---
        selection_layout = QFormLayout()

        self.supplier_combo = QComboBox()
        self.product_combo = QComboBox()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(9999)
        self.price_spin = QDoubleSpinBox() # Price might be fetched or entered
        self.price_spin.setDecimals(2)
        self.price_spin.setMinimum(0.01)
        self.price_spin.setMaximum(99999.99)
        self.btn_add_item = QPushButton("Добавить товар в заказ")

        selection_layout.addRow("Поставщик:", self.supplier_combo)
        selection_layout.addRow("Товар:", self.product_combo)
        selection_layout.addRow("Цена за ед.:", self.price_spin) # Allow manual entry/override
        selection_layout.addRow("Количество:", self.quantity_spin)
        selection_layout.addRow("", self.btn_add_item)

        self.layout.insertLayout(0, selection_layout) # Insert before button box

        # --- Middle Section: Order Items Table ---
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(5) # Product ID, Name, Qty, Unit Price, Total
        self.order_items_table.setHorizontalHeaderLabels(["ID Товара", "Название", "Кол-во", "Цена", "Итого"])
        self.order_items_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.order_items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.order_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.order_items_table.verticalHeader().setVisible(False)
        self.layout.insertWidget(1, self.order_items_table)

        # Добавляем кнопку удаления товара
        remove_button_layout = QHBoxLayout()
        self.btn_remove_item = QPushButton("Удалить выбранный товар")
        self.btn_remove_item.setStyleSheet("background-color: #d32f2f; color: white;")
        remove_button_layout.addStretch()
        remove_button_layout.addWidget(self.btn_remove_item)
        self.layout.insertLayout(2, remove_button_layout)

        # --- Bottom Section: Total Amount and Buttons ---
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Общая сумма заказа: 0.00")
        total_layout.addStretch()
        total_layout.addWidget(self.total_label)
        self.layout.insertLayout(3, total_layout)
        
        # --- Load Data & Connect Signals ---
        self.load_suppliers()
        self.load_products()
        self.btn_add_item.clicked.connect(self.add_item_to_order)
        self.btn_remove_item.clicked.connect(self.remove_item_from_order)
        self.product_combo.currentIndexChanged.connect(self.update_price_from_product) # Auto-fill price

    def load_suppliers(self):
        try:
            self.supplier_combo.clear()
            self.db.cursor.execute("SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name")
            suppliers = self.db.cursor.fetchall()
            if not suppliers:
                self.supplier_combo.addItem("Нет доступных поставщиков", -1)
                self.supplier_combo.setEnabled(False)
            else:
                self.supplier_combo.addItem("Выберите поставщика...", -1)
                for supplier_id, name in suppliers:
                    self.supplier_combo.addItem(name, supplier_id)
        except Exception as e:
            logging.error(f"Ошибка загрузки поставщиков для диалога: {e}")
            QMessageBox.critical(self, "Ошибка БД", "Не удалось загрузить список поставщиков.")

    def load_products(self):
        try:
            self.product_combo.clear()
            # Store price along with ID and name
            self.db.cursor.execute("SELECT product_id, product_name, unit_price FROM products ORDER BY product_name")
            products = self.db.cursor.fetchall()
            if not products:
                self.product_combo.addItem("Нет доступных товаров", -1)
                self.product_combo.setEnabled(False)
            else:
                self.product_combo.addItem("Выберите товар...", (-1, 0.0))
                for product_id, name, price in products:
                    self.product_combo.addItem(name, (product_id, float(price)))
        except Exception as e:
            logging.error(f"Ошибка загрузки товаров для диалога: {e}")
            QMessageBox.critical(self, "Ошибка БД", "Не удалось загрузить список товаров.")

    def update_price_from_product(self, index):
        if index > 0:  # Ignore placeholder
            data = self.product_combo.itemData(index)
            if isinstance(data, tuple) and len(data) == 2:
                product_id, unit_price = data
                if product_id != -1:
                    self.price_spin.setValue(unit_price)

    def add_item_to_order(self):
        product_index = self.product_combo.currentIndex()
        if product_index <= 0:  # Placeholder selected
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар.")
            return

        data = self.product_combo.itemData(product_index)
        if isinstance(data, tuple) and len(data) == 2:
            product_id, _ = data  # игнорируем price из tuple, используем введенный price
        else:
            # Если данные в другом формате
            product_id = data
            
        product_name = self.product_combo.currentText()
        quantity = self.quantity_spin.value()
        entered_price = self.price_spin.value()  # Use entered/updated price

        if quantity <= 0 or entered_price <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество и цена должны быть больше нуля.")
            return

        # Check if product already in table
        for row in range(self.order_items_table.rowCount()):
            if self.order_items_table.item(row, 0).text() == str(product_id):
                QMessageBox.warning(self, "Дубликат", f"Товар '{product_name}' уже добавлен в заказ.")
                return

        # Add row to table
        row_count = self.order_items_table.rowCount()
        self.order_items_table.insertRow(row_count)

        total_item_price = quantity * entered_price

        self.order_items_table.setItem(row_count, 0, QTableWidgetItem(str(product_id)))
        self.order_items_table.setItem(row_count, 1, QTableWidgetItem(product_name))
        self.order_items_table.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
        self.order_items_table.setItem(row_count, 3, QTableWidgetItem(f"{entered_price:.2f}"))
        self.order_items_table.setItem(row_count, 4, QTableWidgetItem(f"{total_item_price:.2f}"))

        self.update_total_amount()
        # Reset selection fields
        self.product_combo.setCurrentIndex(0)
        self.quantity_spin.setValue(1)
        self.price_spin.setValue(0.01)

    def remove_item_from_order(self):
        """Удаление выбранного товара из таблицы заказа"""
        selected_rows = self.order_items_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления из заказа")
            return
            
        # Получение номера строки
        row = selected_rows[0].row()
        product_name = self.order_items_table.item(row, 1).text()
        
        # Подтверждение удаления
        if QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы действительно хотите удалить товар '{product_name}' из заказа?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            # Удаление строки
            self.order_items_table.removeRow(row)
            # Обновление общей суммы
            self.update_total_amount()

    def update_total_amount(self):
        total = 0.0
        for row in range(self.order_items_table.rowCount()):
            try:
                total += float(self.order_items_table.item(row, 4).text())
            except (ValueError, AttributeError):
                pass # Ignore if cell is empty or invalid
        self.total_label.setText(f"Общая сумма заказа: {total:.2f}")

    def get_data(self):
        supplier_index = self.supplier_combo.currentIndex()
        if supplier_index <= 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите поставщика.")
            return None

        supplier_id = self.supplier_combo.itemData(supplier_index)
        items = []
        total_order_amount = 0.0

        if self.order_items_table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар в заказ.")
            return None

        for row in range(self.order_items_table.rowCount()):
            try:
                item_data = {
                    "product_id": int(self.order_items_table.item(row, 0).text()),
                    "quantity": int(self.order_items_table.item(row, 2).text()),
                    "unit_price": float(self.order_items_table.item(row, 3).text()),
                    "total_price": float(self.order_items_table.item(row, 4).text())
                }
                items.append(item_data)
                total_order_amount += item_data["total_price"]
            except (ValueError, AttributeError) as e:
                QMessageBox.critical(self, "Ошибка данных", f"Ошибка в строке {row+1} таблицы заказа: {e}")
                return None

        return {
            "supplier_id": supplier_id,
            "items": items,
            "total_amount": total_order_amount
        }

    # Оставляем для совместимости
    def get_order_data(self):
        return self.get_data()

# Класс диалогового окна для добавления склада
class AddWarehouseDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, db=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Добавить склад")
        # Установка минимальной ширины окна
        self.setMinimumWidth(400)
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Новый склад")
        # Выравнивание заголовка по центру
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка шрифта для заголовка
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Установка стиля для заголовка
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        # Добавление заголовка в макет
        layout.addWidget(title)
        
        # Создание макета формы
        form = QFormLayout()
        
        # Создание поля для ввода названия склада
        self.name_input = QLineEdit()
        # Установка подсказки для поля
        self.name_input.setPlaceholderText("Введите название склада")
        # Добавление поля в форму с меткой
        form.addRow("Название:", self.name_input)
        
        # Создание поля для ввода адреса
        self.location_input = QLineEdit()
        # Установка подсказки для поля
        self.location_input.setPlaceholderText("Введите местоположение")
        # Добавление поля в форму с меткой
        form.addRow("Адрес:", self.location_input)
        
        # Создание поля для ввода вместимости
        self.capacity_input = QSpinBox()
        # Установка диапазона значений вместимости
        self.capacity_input.setRange(1, 1000000)
        # Установка значения по умолчанию
        self.capacity_input.setValue(1000)
        # Установка шага изменения значения
        self.capacity_input.setSingleStep(100)
        # Добавление поля в форму с меткой
        form.addRow("Вместимость:", self.capacity_input)
        
        # Добавление формы в основной макет
        layout.addLayout(form)
        
        # Создание панели кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Подключение сигналов к кнопкам
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление панели кнопок в макет
        layout.addWidget(button_box)
        # Установка макета для окна
        self.setLayout(layout)
    
    # Метод для получения данных о складе
    def get_warehouse_data(self):
        # Возврат словаря с данными склада
        return {
            "name": self.name_input.text(),
            "location": self.location_input.text(),
            "capacity": self.capacity_input.value()
        }

# Класс диалогового окна для подтверждения действий
class ConfirmDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, title="Подтверждение", message="Вы уверены?"):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Установка заголовка окна
        self.setWindowTitle(title)
        
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание метки с сообщением
        label = QLabel(message)
        # Выравнивание сообщения по центру
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Добавление метки в макет
        layout.addWidget(label)
        
        # Создание горизонтального макета для кнопок
        button_box = QHBoxLayout()
        
        # Создание кнопки "Да"
        yes_button = QPushButton("Да")
        # Подключение сигнала нажатия к кнопке
        yes_button.clicked.connect(self.accept)
        
        # Создание кнопки "Нет"
        no_button = QPushButton("Нет")
        # Подключение сигнала нажатия к кнопке
        no_button.clicked.connect(self.reject)
        
        # Добавление кнопок в макет
        button_box.addWidget(yes_button)
        button_box.addWidget(no_button)
        
        # Добавление макета кнопок в основной макет
        layout.addLayout(button_box)
        # Установка макета для окна
        self.setLayout(layout)

# Класс диалогового окна для экспорта данных
class ExportDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, title="Экспорт данных"):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Установка заголовка окна
        self.setWindowTitle(title)
        # Инициализация пути к файлу
        self.file_path = ""
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Экспорт данных")
        # Выравнивание заголовка по центру
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка шрифта для заголовка
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Установка стиля для заголовка
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        # Добавление заголовка в макет
        layout.addWidget(title)
        
        # Создание макета для выбора файла
        file_layout = QHBoxLayout()
        # Создание поля для отображения пути к файлу
        self.file_input = QLineEdit()
        # Установка поля только для чтения
        self.file_input.setReadOnly(True)
        # Установка подсказки для поля
        self.file_input.setPlaceholderText("Выберите путь для сохранения...")
        
        # Создание кнопки для выбора файла
        browse_button = QPushButton("Обзор...")
        # Подключение сигнала нажатия к кнопке
        browse_button.clicked.connect(self.browse_file)
        
        # Добавление элементов в макет выбора файла
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        
        # Добавление макета выбора файла в основной макет
        layout.addLayout(file_layout)
        
        # Создание макета для выбора формата экспорта
        format_layout = QHBoxLayout()
        # Создание метки для выбора формата
        format_label = QLabel("Формат экспорта:")
        
        # Создание выпадающего списка для выбора формата
        self.format_combo = QComboBox()
        # Добавление форматов в выпадающий список
        self.format_combo.addItems(["Excel (.xlsx)", "CSV (.csv)", "PDF (.pdf)"])
        
        # Добавление элементов в макет выбора формата
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        
        # Добавление макета выбора формата в основной макет
        layout.addLayout(format_layout)
        
        # Создание панели кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Подключение сигналов к кнопкам
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление панели кнопок в макет
        layout.addWidget(button_box)
        # Установка макета для окна
        self.setLayout(layout)
    
    # Метод для выбора файла
    def browse_file(self):
        # Словарь с форматами файлов
        formats = {
            0: "Excel Files (*.xlsx)",
            1: "CSV Files (*.csv)",
            2: "PDF Files (*.pdf)"
        }
        # Получение текущего выбранного формата
        current_format = self.format_combo.currentIndex()
        
        # Получаем название вкладки из заголовка диалога
        tab_name = self.windowTitle().replace("Экспорт ", "Экспорт_").replace("данных", "").strip().lower()
        if not tab_name:
            tab_name = "export"
        
        # Формирование имени файла по умолчанию, используя название вкладки вместо "export"
        default_name = f"{tab_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Открытие диалога выбора файла
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Сохранить файл",
            default_name,
            formats[current_format]
        )
        
        # Если файл выбран, сохраняем путь и отображаем его
        if file_path:
            self.file_path = file_path
            self.file_input.setText(file_path)
    
    # Метод для получения данных об экспорте
    def get_export_data(self):
        # Возврат словаря с данными экспорта
        return {
            "file_path": self.file_path,
            "format": self.format_combo.currentText()
        }

# Класс диалогового окна для отправки email
class EmailDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Установка заголовка окна
        self.setWindowTitle("Отправить Email")
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Отправка Email")
        # Выравнивание заголовка по центру
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка шрифта для заголовка
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        # Установка стиля для заголовка
        title.setStyleSheet("color: #2e7d32; margin-bottom: 15px;")
        # Добавление заголовка в макет
        layout.addWidget(title)
        
        # Создание макета формы
        form = QFormLayout()
        
        # Создание поля для ввода адреса получателя
        self.to_input = QLineEdit()
        # Установка подсказки для поля
        self.to_input.setPlaceholderText("Введите email получателя")
        # Добавление поля в форму с меткой
        form.addRow("Кому:", self.to_input)
        
        # Создание поля для ввода темы письма
        self.subject_input = QLineEdit()
        # Установка подсказки для поля
        self.subject_input.setPlaceholderText("Введите тему письма")
        # Добавление поля в форму с меткой
        form.addRow("Тема:", self.subject_input)
        
        # Создание поля для ввода сообщения
        self.message_input = QTextEdit()
        # Установка подсказки для поля
        self.message_input.setPlaceholderText("Введите текст сообщения")
        # Добавление поля в форму с меткой
        form.addRow("Сообщение:", self.message_input)
        
        layout.addLayout(form)
        
        # Создание панели кнопок
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        # Подключение сигналов к кнопкам
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Добавление панели кнопок в макет
        layout.addWidget(button_box)
        # Установка макета для окна
        self.setLayout(layout)
    
    # Метод для получения данных email
    def get_email_data(self):
        # Возврат словаря с данными email
        return {
            "to": self.to_input.text(),
            "subject": self.subject_input.text(),
            "message": self.message_input.toPlainText()
        }
    
class CreatePurchaseOrderDialog(BaseDialog):
    """Dialog to create a new purchase order."""
    def __init__(self, db, parent=None):
        super().__init__("Создать заказ поставщику", parent)
        self.db = db
        self.setMinimumSize(600, 500)

        # --- Top Section: Supplier and Product Selection ---
        selection_layout = QFormLayout()

        self.supplier_combo = QComboBox()
        self.product_combo = QComboBox()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(9999)
        self.price_spin = QDoubleSpinBox() # Price might be fetched or entered
        self.price_spin.setDecimals(2)
        self.price_spin.setMinimum(0.01)
        self.price_spin.setMaximum(99999.99)
        self.btn_add_item = QPushButton("Добавить товар в заказ")

        selection_layout.addRow("Поставщик:", self.supplier_combo)
        selection_layout.addRow("Товар:", self.product_combo)
        selection_layout.addRow("Цена за ед.:", self.price_spin) # Allow manual entry/override
        selection_layout.addRow("Количество:", self.quantity_spin)
        selection_layout.addRow("", self.btn_add_item)

        self.layout.insertLayout(0, selection_layout) # Insert before button box

        # --- Middle Section: Order Items Table ---
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(5) # Product ID, Name, Qty, Unit Price, Total
        self.order_items_table.setHorizontalHeaderLabels(["ID Товара", "Название", "Кол-во", "Цена", "Итого"])
        self.order_items_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.order_items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.order_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.order_items_table.verticalHeader().setVisible(False)
        self.layout.insertWidget(1, self.order_items_table)

        # Добавляем кнопку удаления товара
        remove_button_layout = QHBoxLayout()
        self.btn_remove_item = QPushButton("Удалить выбранный товар")
        self.btn_remove_item.setStyleSheet("background-color: #d32f2f; color: white;")
        remove_button_layout.addStretch()
        remove_button_layout.addWidget(self.btn_remove_item)
        self.layout.insertLayout(2, remove_button_layout)

        # --- Bottom Section: Total Amount and Buttons ---
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Общая сумма заказа: 0.00")
        total_layout.addStretch()
        total_layout.addWidget(self.total_label)
        self.layout.insertLayout(3, total_layout)
        
        # --- Load Data & Connect Signals ---
        self.load_suppliers()
        self.load_products()
        self.btn_add_item.clicked.connect(self.add_item_to_order)
        self.btn_remove_item.clicked.connect(self.remove_item_from_order)
        self.product_combo.currentIndexChanged.connect(self.update_price_from_product) # Auto-fill price

    def load_suppliers(self):
        try:
            self.supplier_combo.clear()
            self.db.cursor.execute("SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name")
            suppliers = self.db.cursor.fetchall()
            if not suppliers:
                self.supplier_combo.addItem("Нет доступных поставщиков", -1)
                self.supplier_combo.setEnabled(False)
            else:
                self.supplier_combo.addItem("Выберите поставщика...", -1)
                for supplier_id, name in suppliers:
                    self.supplier_combo.addItem(name, supplier_id)
        except Exception as e:
            logging.error(f"Ошибка загрузки поставщиков для диалога: {e}")
            QMessageBox.critical(self, "Ошибка БД", "Не удалось загрузить список поставщиков.")

    def load_products(self):
        try:
            self.product_combo.clear()
            # Store price along with ID and name
            self.db.cursor.execute("SELECT product_id, product_name, unit_price FROM products ORDER BY product_name")
            products = self.db.cursor.fetchall()
            if not products:
                self.product_combo.addItem("Нет доступных товаров", -1)
                self.product_combo.setEnabled(False)
            else:
                self.product_combo.addItem("Выберите товар...", (-1, 0.0))
                for product_id, name, price in products:
                    self.product_combo.addItem(name, (product_id, float(price)))
        except Exception as e:
            logging.error(f"Ошибка загрузки товаров для диалога: {e}")
            QMessageBox.critical(self, "Ошибка БД", "Не удалось загрузить список товаров.")

    def update_price_from_product(self, index):
        if index > 0: # Ignore placeholder
            data = self.product_combo.itemData(index)
            if isinstance(data, tuple) and len(data) == 2:
                product_id, unit_price = data
                if product_id != -1:
                    self.price_spin.setValue(unit_price)

    def add_item_to_order(self):
        product_index = self.product_combo.currentIndex()
        if product_index <= 0: # Placeholder selected
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар.")
            return

        data = self.product_combo.itemData(product_index)
        if isinstance(data, tuple) and len(data) == 2:
            product_id, _ = data  # игнорируем price из tuple, используем введенный price
        else:
            # Если данные в другом формате
            product_id = data
            
        product_name = self.product_combo.currentText()
        quantity = self.quantity_spin.value()
        entered_price = self.price_spin.value()  # Use entered/updated price

        if quantity <= 0 or entered_price <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество и цена должны быть больше нуля.")
            return

        # Check if product already in table
        for row in range(self.order_items_table.rowCount()):
            if self.order_items_table.item(row, 0).text() == str(product_id):
                QMessageBox.warning(self, "Дубликат", f"Товар '{product_name}' уже добавлен в заказ.")
                return

        # Add row to table
        row_count = self.order_items_table.rowCount()
        self.order_items_table.insertRow(row_count)

        total_item_price = quantity * entered_price

        self.order_items_table.setItem(row_count, 0, QTableWidgetItem(str(product_id)))
        self.order_items_table.setItem(row_count, 1, QTableWidgetItem(product_name))
        self.order_items_table.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
        self.order_items_table.setItem(row_count, 3, QTableWidgetItem(f"{entered_price:.2f}"))
        self.order_items_table.setItem(row_count, 4, QTableWidgetItem(f"{total_item_price:.2f}"))

        self.update_total_amount()
        # Reset selection fields
        self.product_combo.setCurrentIndex(0)
        self.quantity_spin.setValue(1)
        self.price_spin.setValue(0.01)

    def remove_item_from_order(self):
        """Удаление выбранного товара из таблицы заказа"""
        selected_rows = self.order_items_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления из заказа")
            return
            
        # Получение номера строки
        row = selected_rows[0].row()
        product_name = self.order_items_table.item(row, 1).text()
        
        # Подтверждение удаления
        if QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы действительно хотите удалить товар '{product_name}' из заказа?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            # Удаление строки
            self.order_items_table.removeRow(row)
            # Обновление общей суммы
            self.update_total_amount()

    def update_total_amount(self):
        total = 0.0
        for row in range(self.order_items_table.rowCount()):
            try:
                total += float(self.order_items_table.item(row, 4).text())
            except (ValueError, AttributeError):
                pass # Ignore if cell is empty or invalid
        self.total_label.setText(f"Общая сумма заказа: {total:.2f}")

    def get_data(self):
        supplier_index = self.supplier_combo.currentIndex()
        if supplier_index <= 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите поставщика.")
            return None

        supplier_id = self.supplier_combo.itemData(supplier_index)
        items = []
        total_order_amount = 0.0

        if self.order_items_table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один товар в заказ.")
            return None

        for row in range(self.order_items_table.rowCount()):
            try:
                item_data = {
                    "product_id": int(self.order_items_table.item(row, 0).text()),
                    "quantity": int(self.order_items_table.item(row, 2).text()),
                    "unit_price": float(self.order_items_table.item(row, 3).text()),
                    "total_price": float(self.order_items_table.item(row, 4).text())
                }
                items.append(item_data)
                total_order_amount += item_data["total_price"]
            except (ValueError, AttributeError) as e:
                QMessageBox.critical(self, "Ошибка данных", f"Ошибка в строке {row+1} таблицы заказа: {e}")
                return None

        return {
            "supplier_id": supplier_id,
            "items": items,
            "total_amount": total_order_amount
        }

    # Оставляем для совместимости
    def get_order_data(self):
        return self.get_data() 