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
    Класс для управления складами в системе управления складом.
    Наследуется от QWidget для создания пользовательского интерфейса.
    """

    def __init__(self, db):
        """
        Инициализация вкладки складов.
        
        Args:
            db: Объект базы данных для операций со складами
        """
        super().__init__()
        # Сохранение объекта базы данных
        self.db = db
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Загрузка списка складов
        self.load_warehouses()

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
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Создание таблицы для отображения складов
        self.warehouses_table = QTableWidget()
        self.warehouses_table.setColumnCount(4)
        self.warehouses_table.setHorizontalHeaderLabels([
            "ID", "Название", "Местоположение", "Вместимость"
        ])
        # Настройка автоматического изменения размера столбцов
        self.warehouses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Настройка автоматического изменения размера строк
        self.warehouses_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создание нижней панели с дополнительными функциями
        bottom_panel = QHBoxLayout()

        # Создание левой части нижней панели - кнопки с иконками
        left_button_panel = QHBoxLayout()

        # Создание кнопки обновления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Создание кнопки просмотра запасов
        self.btn_stock = QPushButton("Запасы на складе")
        self.btn_stock.setIcon(QIcon.fromTheme("document-properties"))

        # Добавление кнопок на левую панель
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_stock)
        left_button_panel.addStretch()

        # Создание правой части нижней панели - кнопка экспорта и счетчик
        right_button_panel = QHBoxLayout()
        
        # Создание метки с количеством складов
        self.warehouse_count_label = QLabel("Всего складов: 0")
        
        # Создание кнопки экспорта
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Добавление элементов на правую панель
        right_button_panel.addWidget(self.warehouse_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Сборка нижней панели из левой и правой частей
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Сборка основного интерфейса
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.warehouses_table)
        main_layout.addLayout(bottom_panel)

        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.add_warehouse)
        self.btn_delete.clicked.connect(self.delete_warehouse)
        self.btn_edit.clicked.connect(self.edit_warehouse)
        self.btn_refresh.clicked.connect(self.load_warehouses)
        self.btn_stock.clicked.connect(self.show_warehouse_stock)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_warehouses(self):
        """Загрузка складов из базы данных и отображение в таблице"""
        try:
            # SQL-запрос для получения списка складов
            query = """
                SELECT warehouse_id, warehouse_name, location, capacity
                FROM warehouses
                ORDER BY warehouse_name
            """
            # Получение списка складов из базы данных
            warehouses = self.db.fetch_all(query)

            # Установка количества строк в таблице
            self.warehouses_table.setRowCount(len(warehouses))

            # Заполнение таблицы данными
            for row_idx, warehouse in enumerate(warehouses):
                for col_idx, data in enumerate(warehouse):
                    # Создание элемента таблицы
                    item = QTableWidgetItem(str(data))
                    # Запрет редактирования ячеек
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    # Установка элемента в таблицу
                    self.warehouses_table.setItem(row_idx, col_idx, item)
                    
            # Обновление счетчика складов
            self.warehouse_count_label.setText(f"Всего складов: {len(warehouses)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки складов: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о складах")

    def handle_search(self):
        """Обработка поиска складов"""
        try:
            # Получение текста поиска
            search_text = self.search.text()

            # SQL-запрос для поиска складов
            query = """
                SELECT warehouse_id, warehouse_name, location, capacity
                FROM warehouses
                WHERE warehouse_name ILIKE %s OR location ILIKE %s
                ORDER BY warehouse_name
            """
            # Параметр поиска
            search_param = f"%{search_text}%"
            # Выполнение поиска
            warehouses = self.db.fetch_all(query, (search_param, search_param))

            # Установка количества строк в таблице
            self.warehouses_table.setRowCount(len(warehouses))

            # Заполнение таблицы результатами поиска
            for row_idx, warehouse in enumerate(warehouses):
                for col_idx, data in enumerate(warehouse):
                    item = QTableWidgetItem(str(data))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.warehouses_table.setItem(row_idx, col_idx, item)
                    
            # Обновление счетчика для результатов поиска
            self.warehouse_count_label.setText(f"Найдено складов: {len(warehouses)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка поиска складов: {str(e)}")

    def add_warehouse(self):
        """Отображение диалога добавления нового склада"""
        # Создание диалога добавления склада
        dialog = AddWarehouseDialog(self, self.db)
        if dialog.exec():
            # Получение данных склада из диалога
            warehouse_data = dialog.get_warehouse_data()
            try:
                # SQL-запрос для добавления склада
                query = """
                    INSERT INTO warehouses (warehouse_name, location, capacity)
                    VALUES (%s, %s, %s)
                """
                # Параметры запроса
                params = (
                    warehouse_data["name"],
                    warehouse_data["location"],
                    warehouse_data["capacity"]
                )
                # Выполнение запроса
                success = self.db.execute_query(query, params)
                if success:
                    # Обновление списка складов
                    self.load_warehouses()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Склад успешно добавлен")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить склад")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка добавления склада: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить склад: {str(e)}")

    def delete_warehouse(self):
        """Удаление выбранного склада"""
        # Получение выбранных строк
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если склад не выбран
            QMessageBox.warning(self, "Внимание", "Выберите склад для удаления")
            return

        # Получение номера строки и ID склада
        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()
        # Получение названия склада
        warehouse_name = self.warehouses_table.item(row, 1).text()

        # Проверка наличия товаров на складе
        try:
            # SQL-запрос для проверки наличия товаров
            check_query = "SELECT COUNT(*) FROM stock WHERE warehouse_id = %s"
            count = self.db.fetch_one(check_query, (warehouse_id,))
            
            if count and count[0] > 0:
                # Отображение предупреждения о наличии товаров
                QMessageBox.warning(
                    self, 
                    "Внимание", 
                    f"Склад '{warehouse_name}' содержит товары и не может быть удален."
                )
                return
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка проверки товаров на складе: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось проверить содержимое склада: {str(e)}")
            return

        # Создание диалога подтверждения
        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить склад:\n{warehouse_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                # SQL-запрос для удаления склада
                query = "DELETE FROM warehouses WHERE warehouse_id = %s"
                # Выполнение запроса
                success = self.db.execute_query(query, (warehouse_id,))
                if success:
                    # Обновление списка складов
                    self.load_warehouses()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Склад успешно удален")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить склад")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка удаления склада: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить склад: {str(e)}")

    def edit_warehouse(self):
        """Редактирование выбранного склада"""
        # Получение выбранных строк
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если склад не выбран
            QMessageBox.warning(self, "Внимание", "Выберите склад для редактирования")
            return

        # Получение номера строки и ID склада
        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()

        try:
            # SQL-запрос для получения данных склада
            query = """
                SELECT warehouse_name, location, capacity 
                FROM warehouses 
                WHERE warehouse_id = %s
            """
            # Получение данных склада
            warehouse = self.db.fetch_one(query, (warehouse_id,))
            
            if warehouse:
                # Создание диалога редактирования
                dialog = AddWarehouseDialog(self, self.db)
                dialog.setWindowTitle("Редактировать склад")
                
                # Заполнение полей диалога текущими данными
                dialog.name_input.setText(warehouse[0])
                dialog.location_input.setText(warehouse[1])
                dialog.capacity_input.setValue(int(warehouse[2]))

                if dialog.exec():
                    # Получение обновленных данных
                    updated_data = dialog.get_warehouse_data()
                    # SQL-запрос для обновления склада
                    update_query = """
                        UPDATE warehouses 
                        SET warehouse_name = %s, 
                            location = %s, 
                            capacity = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE warehouse_id = %s
                    """
                    # Параметры запроса
                    update_params = (
                        updated_data["name"],
                        updated_data["location"],
                        updated_data["capacity"],
                        warehouse_id
                    )
                    # Выполнение запроса
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        # Обновление списка складов
                        self.load_warehouses()
                        # Отображение сообщения об успехе
                        QMessageBox.information(self, "Успех", "Данные склада успешно обновлены")
                    else:
                        # Отображение сообщения об ошибке
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные склада")
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка редактирования склада: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать склад: {str(e)}")

    def show_warehouse_stock(self):
        """Отображение товаров на выбранном складе"""
        # Получение выбранных строк
        selected_rows = self.warehouses_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если склад не выбран
            QMessageBox.warning(self, "Внимание", "Выберите склад для просмотра запасов")
            return

        # Получение данных о складе
        row = selected_rows[0].row()
        warehouse_id = self.warehouses_table.item(row, 0).text()
        warehouse_name = self.warehouses_table.item(row, 1).text()
        
        try:
            # SQL-запрос для получения товаров на складе
            query = """
                SELECT p.product_name, s.quantity, p.category, p.unit_price
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                WHERE s.warehouse_id = %s
                ORDER BY p.product_name
            """
            # Получение списка товаров
            stock_items = self.db.fetch_all(query, (warehouse_id,))
            
            if not stock_items:
                # Отображение сообщения, если товаров нет
                QMessageBox.information(self, "Запасы на складе", f"На складе {warehouse_name} нет товаров")
                return
                
            # Форматирование текста с информацией о товарах
            details_text = f"Товары на складе: {warehouse_name}\n\n"
            details_text += "Товар | Количество | Категория | Цена\n"
            details_text += "--------------------------------\n"
            
            # Инициализация счетчиков
            total_items = 0
            total_value = 0
            
            # Добавление информации о каждом товаре
            for item in stock_items:
                product_name, quantity, category, price = item
                # Расчет стоимости товара
                item_value = quantity * price
                # Обновление счетчиков
                total_items += quantity
                total_value += item_value
                
                # Добавление строки с информацией о товаре
                details_text += f"{product_name} | {quantity} | {category} | {price}₽\n"
                
            # Добавление итоговой информации
            details_text += "--------------------------------\n"
            details_text += f"Всего товаров: {total_items}\n"
            details_text += f"Общая стоимость: {total_value}₽"
                
            # Отображение информации о товарах
            QMessageBox.information(self, "Запасы на складе", details_text)
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка отображения запасов склада: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить запасы склада: {str(e)}")

    def export_data(self):
        """Экспорт данных о складах"""
        # Простая реализация - в реальном приложении использовалась бы функциональность экспорта
        QMessageBox.information(self, "Экспорт", "Функция экспорта пока не реализована") 