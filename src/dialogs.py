# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QComboBox, QDateEdit, QSpinBox,
                             QDoubleSpinBox, QGridLayout, QFormLayout, QTextEdit, QDialogButtonBox,
                             QFileDialog)
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
class AddOrderDialog(QDialog):
    # Инициализация класса
    def __init__(self, parent=None, db=None):
        # Вызов конструктора родительского класса
        super().__init__(parent)
        # Сохранение объекта базы данных
        self.db = db
        # Установка заголовка окна
        self.setWindowTitle("Создать заказ")
        # Установка минимальной ширины окна
        self.setMinimumWidth(450)
        # Инициализация списка поставщиков
        self.suppliers = []
        # Загрузка списка поставщиков из базы данных
        self.load_suppliers()
        # Настройка пользовательского интерфейса
        self.setup_ui()
        
    # Метод загрузки списка поставщиков из базы данных
    def load_suppliers(self):
        # Проверка наличия объекта базы данных
        if self.db:
            try:
                # SQL-запрос для получения списка поставщиков
                query = "SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name"
                # Получение списка поставщиков из базы данных
                self.suppliers = self.db.fetch_all(query)
            except Exception as e:
                # Логирование ошибки при загрузке поставщиков
                logging.error(f"Error loading suppliers: {str(e)}")
                # Инициализация пустого списка в случае ошибки
                self.suppliers = []
    
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        # Создание вертикального макета
        layout = QVBoxLayout()
        
        # Создание заголовка
        title = QLabel("Новый заказ")
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
        
        # Создание поля для выбора даты заказа
        self.date_input = QDateEdit()
        # Установка текущей даты по умолчанию
        self.date_input.setDate(QDate.currentDate())
        # Включение всплывающего календаря
        self.date_input.setCalendarPopup(True)
        # Добавление поля в форму с меткой
        form.addRow("Дата заказа:", self.date_input)
        
        # Создание выпадающего списка для выбора поставщика
        self.supplier_input = QComboBox()
        # Добавление поставщиков в выпадающий список
        for supplier_id, supplier_name in self.suppliers:
            self.supplier_input.addItem(supplier_name, supplier_id)
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Поставщик:", self.supplier_input)
        
        # Создание поля для ввода суммы заказа
        self.amount_input = QDoubleSpinBox()
        # Установка диапазона значений суммы
        self.amount_input.setRange(0.01, 10000000.00)
        # Установка значения по умолчанию
        self.amount_input.setValue(0.01)
        # Установка шага изменения значения
        self.amount_input.setSingleStep(100.00)
        # Добавление символа валюты
        self.amount_input.setPrefix("₽ ")
        # Добавление поля в форму с меткой
        form.addRow("Сумма заказа:", self.amount_input)
        
        # Создание выпадающего списка для выбора статуса
        self.status_input = QComboBox()
        # Список возможных статусов заказа
        statuses = ["в обработке", "доставлен", "отменен"]
        # Добавление статусов в выпадающий список
        self.status_input.addItems(statuses)
        # Добавление выпадающего списка в форму с меткой
        form.addRow("Статус:", self.status_input)
        
        # Создание поля для ввода примечания
        self.note_input = QTextEdit()
        # Установка подсказки для поля
        self.note_input.setPlaceholderText("Введите примечание к заказу (необязательно)")
        # Установка максимальной высоты поля
        self.note_input.setMaximumHeight(80)
        # Добавление поля в форму с меткой
        form.addRow("Примечание:", self.note_input)
        
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
    
    # Метод для получения данных о заказе
    def get_order_data(self):
        # Возврат словаря с данными заказа
        return {
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "supplier_id": self.supplier_input.currentData(),
            "amount": self.amount_input.value(),
            "status": self.status_input.currentText(),
            "note": self.note_input.toPlainText()
        }

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