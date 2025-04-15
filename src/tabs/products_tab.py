from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QHeaderView, QMessageBox, 
    QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import logging
from dialogs import AddProductDialog, ConfirmDialog, ExportDialog
from data_export import DataExporter

class ProductsTab(QWidget):
    """
    Класс для управления товарами в системе управления складом.
    Наследуется от QWidget для создания пользовательского интерфейса.
    """

    def __init__(self, db):
        """
        Инициализация вкладки товаров.
        
        Args:
            db: Объект базы данных для операций с товарами
        """
        super().__init__()
        # Сохранение объекта базы данных
        self.db = db
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Загрузка списка товаров
        self.load_products()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Создание основного вертикального макета
        main_layout = QVBoxLayout()

        # Создание верхней панели с кнопками управления
        top_panel = QHBoxLayout()

        # Создание кнопок управления
        self.btn_add = QPushButton("Добавить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_edit = QPushButton("Редактировать")

        # Создание поля поиска
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        # Добавление растягивающегося элемента
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавление элементов на верхнюю панель
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_delete)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.search)
        top_panel.addItem(spacer)

        # Создание таблицы для отображения товаров
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Название", "Категория", "Цена", "Описание"])
        # Настройка автоматического изменения размера столбцов
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Настройка автоматического изменения размера строк
        self.products_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создание нижней панели с дополнительными функциями
        bottom_panel = QHBoxLayout()

        # Создание левой части нижней панели - кнопки с иконками
        left_button_panel = QHBoxLayout()

        # Создание кнопки обновления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Создание кнопки статистики
        self.btn_stats = QPushButton("Статистика")
        self.btn_stats.setIcon(QIcon.fromTheme("document-properties"))

        # Добавление кнопок на левую панель
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_stats)
        left_button_panel.addStretch()

        # Создание правой части нижней панели - кнопка экспорта
        right_button_panel = QHBoxLayout()
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Добавление элементов на правую панель
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Сборка нижней панели из левой и правой частей
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Сборка основного интерфейса
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.products_table)
        main_layout.addLayout(bottom_panel)

        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.add_product)
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_edit.clicked.connect(self.edit_product)
        self.btn_refresh.clicked.connect(self.load_products)
        self.btn_stats.clicked.connect(self.show_stats)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_products(self):
        """Загрузка товаров из базы данных и отображение в таблице"""
        try:
            # SQL-запрос для получения списка товаров
            query = "SELECT product_id, product_name, category, unit_price, product_description FROM products ORDER BY product_name"
            # Получение списка товаров из базы данных
            products = self.db.fetch_all(query)

            # Установка количества строк в таблице
            self.products_table.setRowCount(len(products))

            # Заполнение таблицы данными
            for row_idx, product in enumerate(products):
                for col_idx, data in enumerate(product):
                    # Создание элемента таблицы
                    item = QTableWidgetItem(str(data))
                    # Запрет редактирования ячеек
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    # Установка элемента в таблицу
                    self.products_table.setItem(row_idx, col_idx, item)
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки товаров: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о товарах")

    def handle_search(self):
        """Обработка поиска товаров по введенному тексту"""
        try:
            # Получение текста поиска
            search_text = self.search.text()

            # SQL-запрос для поиска товаров
            query = """
                SELECT product_id, product_name, category, unit_price, product_description 
                FROM products 
                WHERE product_name ILIKE %s 
                   OR category ILIKE %s 
                   OR product_description ILIKE %s
                ORDER BY product_name
            """
            # Выполнение поиска
            products = self.db.fetch_all(query, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))

            # Установка количества строк в таблице
            self.products_table.setRowCount(len(products))

            # Заполнение таблицы результатами поиска
            for row_idx, product in enumerate(products):
                for col_idx, data in enumerate(product):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.products_table.setItem(row_idx, col_idx, item)
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка поиска товаров: {str(e)}")

    def add_product(self):
        """Отображение диалога добавления нового товара"""
        # Создание диалога добавления товара
        dialog = AddProductDialog(self, self.db)
        if dialog.exec():
            # Получение данных товара из диалога
            product_data = dialog.get_product_data()
            try:
                # SQL-запрос для добавления товара
                query = """
                    INSERT INTO products (product_name, product_description, category, unit_price)
                    VALUES (%s, %s, %s, %s)
                """
                # Параметры запроса
                params = (
                    product_data["name"],
                    product_data["description"],
                    product_data["category"],
                    product_data["price"]
                )
                # Выполнение запроса
                success = self.db.execute_query(query, params)
                if success:
                    # Обновление списка товаров
                    self.load_products()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Товар успешно добавлен")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить товар")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка добавления товара: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар: {str(e)}")

    def delete_product(self):
        """Удаление выбранного товара"""
        # Получение выбранных строк
        selected_rows = self.products_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если товар не выбран
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления")
            return

        # Получение номера строки и ID товара
        row = selected_rows[0].row()
        product_id = self.products_table.item(row, 0).text()
        # Получение названия товара
        product_name = self.products_table.item(row, 1).text()

        # Создание диалога подтверждения
        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить товар:\n{product_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                # SQL-запрос для удаления товара
                query = "DELETE FROM products WHERE product_id = %s"
                # Выполнение запроса
                success = self.db.execute_query(query, (product_id,))
                if success:
                    # Обновление списка товаров
                    self.load_products()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Товар успешно удален")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить товар")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка удаления товара: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить товар: {str(e)}")

    def edit_product(self):
        """Редактирование выбранного товара"""
        # Получение выбранных строк
        selected_rows = self.products_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если товар не выбран
            QMessageBox.warning(self, "Внимание", "Выберите товар для редактирования")
            return

        # Получение номера строки и ID товара
        row = selected_rows[0].row()
        product_id = self.products_table.item(row, 0).text()

        try:
            # Получение данных товара
            query = "SELECT product_name, product_description, category, unit_price FROM products WHERE product_id = %s"
            product = self.db.fetch_one(query, (product_id,))
            
            if product:
                # Создание диалога редактирования
                dialog = AddProductDialog(self, self.db)
                dialog.setWindowTitle("Редактировать товар")
                
                # Заполнение полей диалога текущими данными
                dialog.name_input.setText(product[0])
                dialog.description_input.setText(product[1])
                # Поиск индекса категории
                index = dialog.category_input.findText(product[2])
                if index >= 0:
                    dialog.category_input.setCurrentIndex(index)
                # Установка цены
                dialog.price_input.setValue(float(product[3]))

                if dialog.exec():
                    # Получение обновленных данных
                    updated_data = dialog.get_product_data()
                    # SQL-запрос для обновления товара
                    update_query = """
                        UPDATE products 
                        SET product_name = %s, 
                            product_description = %s, 
                            category = %s, 
                            unit_price = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE product_id = %s
                    """
                    # Параметры запроса
                    update_params = (
                        updated_data["name"],
                        updated_data["description"],
                        updated_data["category"],
                        updated_data["price"],
                        product_id
                    )
                    # Выполнение запроса
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        # Обновление списка товаров
                        self.load_products()
                        # Отображение сообщения об успехе
                        QMessageBox.information(self, "Успех", "Товар успешно обновлен")
                    else:
                        # Отображение сообщения об ошибке
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить товар")
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка редактирования товара: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать товар: {str(e)}")

    def export_data(self):
        """Экспорт данных о товарах"""
        # Создание диалога экспорта
        dialog = ExportDialog(self, "Экспорт товаров")
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
                # SQL-запрос для получения данных о товарах
                query = """
                    SELECT p.product_name, p.product_description, p.category, p.unit_price
                    FROM products p
                    ORDER BY p.product_name
                """
                
                # Заголовки для экспорта
                headers = ["Название", "Описание", "Категория", "Цена"]
                
                # Создание объекта для экспорта
                exporter = DataExporter(self)
                
                # Экспорт в зависимости от выбранного формата
                if "Excel" in export_format:
                    success = exporter.export_to_excel(
                        query=query,
                        filename=file_path,
                        headers=headers,
                        sheet_name="Товары"
                    )
                elif "CSV" in export_format:
                    success = exporter.export_to_csv(
                        query=query,
                        filename=file_path,
                        headers=headers
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
                logging.error(f"Ошибка экспорта товаров: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте данных: {str(e)}")

    def show_stats(self):
        """Отображение статистики по товарам"""
        # Отображение сообщения о том, что функция пока не реализована
        QMessageBox.information(self, "Статистика", "Функция статистики пока не реализована")