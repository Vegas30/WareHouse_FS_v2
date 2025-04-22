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
# Импорт базового класса диалога
from dialogs import BaseDialog

# Класс диалогового окна для работы с запасами
class StockDialog(QDialog):
    """
    Диалоговое окно для добавления и редактирования запасов товара на складе.
    
    :param parent: Родительский виджет
    :type parent: QWidget или None
    :param stock: Данные о запасе для редактирования (id, product_id, warehouse_id, quantity, last_restocked)
    :type stock: tuple или None
    :param products: Список доступных товаров
    :type products: list или None
    :param warehouses: Список доступных складов
    :type warehouses: list или None
    """
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
        """
        Настраивает пользовательский интерфейс диалогового окна.
        Создает и размещает все элементы управления.
        """
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
        """
        Возвращает данные о запасе из полей формы.
        
        :return: Словарь с данными о запасе (product_id, warehouse_id, quantity, restock_date)
        :rtype: dict
        """
        # Возврат словаря с данными запаса
        return {
            "product_id": self.product_combo.currentData(),
            "warehouse_id": self.warehouse_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "restock_date": self.restock_date.date().toString("yyyy-MM-dd")
        }

# Класс диалогового окна для добавления товара
class AddProductDialog(QDialog):
    """
    Диалоговое окно для добавления нового товара в систему.
    
    :param parent: Родительский виджет
    :type parent: QWidget или None
    :param db: Объект базы данных для работы с данными
    :type db: Database или None
    """
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
        """
        Настраивает пользовательский интерфейс диалогового окна.
        Создает и размещает все элементы управления для добавления товара.
        """
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
        """
        Возвращает данные о товаре из полей формы.
        
        :return: Словарь с данными о товаре (name, description, category, price)
        :rtype: dict
        """
        # Возврат словаря с данными товара
        return {
            "name": self.name_input.text(),
            "description": self.description_input.toPlainText(),
            "category": self.category_input.currentText(),
            "price": self.price_input.value()
        }

# Класс диалогового окна для добавления поставщика
class AddSupplierDialog(QDialog):
    """
    Диалоговое окно для добавления нового поставщика в систему.
    
    :param parent: Родительский виджет
    :type parent: QWidget или None
    :param db: Объект базы данных для работы с данными
    :type db: Database или None
    """
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
        """
        Настраивает пользовательский интерфейс диалогового окна.
        Создает и размещает все элементы управления для добавления поставщика.
        """
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
        """
        Возвращает данные о поставщике из полей формы.
        
        :return: Словарь с данными о поставщике (name, contact, phone, email)
        :rtype: dict
        """
        # Возврат словаря с данными поставщика
        return {
            "name": self.name_input.text(),
            "contact": self.contact_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }

# Класс диалогового окна для добавления заказа
class AddOrderDialog(BaseDialog):
    """
    Диалог для создания и редактирования заказов поставщиков.
    
    Позволяет выбрать поставщика, добавить товары в заказ,
    указать количество и цену каждого товара, а также
    посмотреть общую сумму заказа.
    
    :param parent: Родительский виджет
    :type parent: QWidget или None
    :param db: Объект базы данных для работы с данными
    :type db: Database или None
    """
    def __init__(self, parent=None, db=None):
        super().__init__("Создать заказ", parent)
        self.db = db
        self.setMinimumSize(600, 500)

        # --- Верхняя секция: Выбор поставщика и товара ---
        selection_layout = QFormLayout()

        self.supplier_combo = QComboBox()
        self.product_combo = QComboBox()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(9999)
        self.price_spin = QDoubleSpinBox() # Цена может быть получена или введена
        self.price_spin.setDecimals(2)
        self.price_spin.setMinimum(0.01)
        self.price_spin.setMaximum(99999.99)
        self.btn_add_item = QPushButton("Добавить товар в заказ")

        selection_layout.addRow("Поставщик:", self.supplier_combo)
        selection_layout.addRow("Товар:", self.product_combo)
        selection_layout.addRow("Цена за ед.:", self.price_spin) # Разрешить ручной ввод/переопределение
        selection_layout.addRow("Количество:", self.quantity_spin)
        selection_layout.addRow("", self.btn_add_item)

        self.layout.insertLayout(0, selection_layout) # Вставить перед панелью кнопок

        # --- Центральная секция: Таблица с товарами заказа ---
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(5) # ID товара, Название, Количество, Цена за единицу, Итого
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

        # --- Нижняя секция: Общая сумма и кнопки ---
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Общая сумма заказа: 0.00")
        total_layout.addStretch()
        total_layout.addWidget(self.total_label)
        self.layout.insertLayout(3, total_layout)
        
        # --- Загрузка данных и подключение сигналов ---
        self.load_suppliers()
        self.load_products()
        self.btn_add_item.clicked.connect(self.add_item_to_order)
        self.btn_remove_item.clicked.connect(self.remove_item_from_order)
        self.product_combo.currentIndexChanged.connect(self.update_price_from_product) # Автозаполнение цены

    def load_suppliers(self):
        """
        Загружает список поставщиков из базы данных и заполняет выпадающий список.
        
        В случае ошибки выводит сообщение и отключает список поставщиков.
        """
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
        """
        Загружает список товаров из базы данных и заполняет выпадающий список.
        
        Сохраняет информацию о цене товара вместе с его ID для автоматического заполнения.
        В случае ошибки выводит сообщение и отключает список товаров.
        """
        try:
            self.product_combo.clear()
            # Сохраняем цену вместе с ID и названием
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
        """
        Автоматически обновляет поле цены при выборе товара.
        
        :param index: Индекс выбранного элемента в выпадающем списке товаров
        :type index: int
        """
        if index > 0:  # Игнорировать заполнитель
            data = self.product_combo.itemData(index)
            if isinstance(data, tuple) and len(data) == 2:
                product_id, unit_price = data
                if product_id != -1:
                    self.price_spin.setValue(unit_price)

    def add_item_to_order(self):
        """
        Добавляет выбранный товар в таблицу заказа.
        
        Проверяет корректность ввода и наличие дубликатов.
        Обновляет общую сумму заказа.
        """
        product_index = self.product_combo.currentIndex()
        if product_index <= 0:  # Выбран заполнитель
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите товар.")
            return

        data = self.product_combo.itemData(product_index)
        if isinstance(data, tuple) and len(data) == 2:
            product_id, _ = data  # Игнорируем price из tuple, используем введенный price
        else:
            # Если данные в другом формате
            product_id = data
            
        product_name = self.product_combo.currentText()
        quantity = self.quantity_spin.value()
        entered_price = self.price_spin.value()  # Используем введенную/обновленную цену

        if quantity <= 0 or entered_price <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество и цена должны быть больше нуля.")
            return

        # Проверяем, есть ли товар уже в таблице
        for row in range(self.order_items_table.rowCount()):
            if self.order_items_table.item(row, 0).text() == str(product_id):
                QMessageBox.warning(self, "Дубликат", f"Товар '{product_name}' уже добавлен в заказ.")
                return

        # Добавляем строку в таблицу
        row_count = self.order_items_table.rowCount()
        self.order_items_table.insertRow(row_count)

        total_item_price = quantity * entered_price

        self.order_items_table.setItem(row_count, 0, QTableWidgetItem(str(product_id)))
        self.order_items_table.setItem(row_count, 1, QTableWidgetItem(product_name))
        self.order_items_table.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
        self.order_items_table.setItem(row_count, 3, QTableWidgetItem(f"{entered_price:.2f}"))
        self.order_items_table.setItem(row_count, 4, QTableWidgetItem(f"{total_item_price:.2f}"))

        self.update_total_amount()
        # Сбрасываем поля выбора
        self.product_combo.setCurrentIndex(0)
        self.quantity_spin.setValue(1)
        self.price_spin.setValue(0.01)

    def remove_item_from_order(self):
        """
        Удаляет выбранный товар из таблицы заказа.
        
        Запрашивает подтверждение перед удалением и обновляет общую сумму заказа.
        """
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
        """
        Пересчитывает и обновляет общую сумму заказа на основе данных в таблице.
        """
        total = 0.0
        for row in range(self.order_items_table.rowCount()):
            try:
                total += float(self.order_items_table.item(row, 4).text())
            except (ValueError, AttributeError):
                pass # Игнорировать, если ячейка пуста или содержит некорректные данные
        self.total_label.setText(f"Общая сумма заказа: {total:.2f}")

    def get_data(self):
        """
        Собирает все данные заказа из интерфейса.
        
        :return: Словарь с данными заказа или None в случае ошибки
        :rtype: dict или None
        """
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
        """
        Метод-обертка для совместимости со старым кодом.
        
        :return: Результат выполнения метода get_data()
        :rtype: dict или None
        """
        return self.get_data()
