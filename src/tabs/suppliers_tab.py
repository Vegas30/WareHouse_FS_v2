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
    Класс для управления поставщиками в системе управления складом.
    Наследуется от QWidget для создания пользовательского интерфейса.
    """

    def __init__(self, db):
        """
        Инициализация вкладки поставщиков.
        
        Args:
            db: Объект базы данных для операций с поставщиками
        """
        super().__init__()
        # Сохранение объекта базы данных
        self.db = db
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Загрузка списка поставщиков
        self.load_suppliers()

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
        self.btn_email = QPushButton("Отправить письмо")

        # Создание поля поиска
        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        # Добавление растягивающегося элемента
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Добавление элементов на верхнюю панель
        top_panel.addWidget(self.btn_add)
        top_panel.addWidget(self.btn_delete)
        top_panel.addWidget(self.btn_edit)
        top_panel.addWidget(self.btn_email)
        top_panel.addItem(spacer)
        top_panel.addWidget(self.search)

        # Создание таблицы для отображения поставщиков
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(5)
        self.suppliers_table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Контактное лицо", "Телефон", "Email"
        ])
        # Настройка автоматического изменения размера столбцов
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Настройка автоматического изменения размера строк
        self.suppliers_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Создание нижней панели с дополнительными функциями
        bottom_panel = QHBoxLayout()

        # Создание левой части нижней панели - кнопки с иконками
        left_button_panel = QHBoxLayout()

        # Создание кнопки обновления
        self.btn_refresh = QPushButton("Обновить")
        self.btn_refresh.setIcon(QIcon.fromTheme("view-refresh"))
        
        # Создание кнопки заказов
        self.btn_orders = QPushButton("Заказы поставщика")
        self.btn_orders.setIcon(QIcon.fromTheme("document-properties"))

        # Добавление кнопок на левую панель
        left_button_panel.addWidget(self.btn_refresh)
        left_button_panel.addWidget(self.btn_orders)
        left_button_panel.addStretch()

        # Создание правой части нижней панели - кнопка экспорта и счетчик
        right_button_panel = QHBoxLayout()
        
        # Создание метки с количеством поставщиков
        self.supplier_count_label = QLabel("Всего поставщиков: 0")
        
        # Создание кнопки экспорта
        self.btn_export = QPushButton("Экспорт")
        self.btn_export.setIcon(QIcon.fromTheme("document-save"))

        # Добавление элементов на правую панель
        right_button_panel.addWidget(self.supplier_count_label)
        right_button_panel.addStretch()
        right_button_panel.addWidget(self.btn_export)

        # Сборка нижней панели из левой и правой частей
        bottom_panel.addLayout(left_button_panel, stretch=1)
        bottom_panel.addLayout(right_button_panel, stretch=1)

        # Сборка основного интерфейса
        main_layout.addLayout(top_panel)
        main_layout.addWidget(self.suppliers_table)
        main_layout.addLayout(bottom_panel)

        # Установка основного макета
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.btn_add.clicked.connect(self.add_supplier)
        self.btn_delete.clicked.connect(self.delete_supplier)
        self.btn_edit.clicked.connect(self.edit_supplier)
        self.btn_email.clicked.connect(self.send_email)
        self.btn_refresh.clicked.connect(self.load_suppliers)
        self.btn_orders.clicked.connect(self.show_supplier_orders)
        self.btn_export.clicked.connect(self.export_data)
        self.search.textChanged.connect(self.handle_search)

    def load_suppliers(self):
        """Загрузка поставщиков из базы данных и отображение в таблице"""
        try:
            # SQL-запрос для получения списка поставщиков
            query = """
                SELECT supplier_id, supplier_name, contact_person, phone_number, email
                FROM suppliers
                ORDER BY supplier_name
            """
            # Получение списка поставщиков из базы данных
            suppliers = self.db.fetch_all(query)

            # Установка количества строк в таблице
            self.suppliers_table.setRowCount(len(suppliers))

            # Заполнение таблицы данными
            for row_idx, supplier in enumerate(suppliers):
                for col_idx, data in enumerate(supplier):
                    # Создание элемента таблицы
                    item = QTableWidgetItem(str(data) if data else "")
                    # Запрет редактирования ячеек
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    # Установка элемента в таблицу
                    self.suppliers_table.setItem(row_idx, col_idx, item)
            
            # Обновление счетчика поставщиков
            self.supplier_count_label.setText(f"Всего поставщиков: {len(suppliers)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка загрузки поставщиков: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные о поставщиках")

    def handle_search(self):
        """Обработка поиска поставщиков"""
        try:
            # Получение текста поиска
            search_text = self.search.text()

            # SQL-запрос для поиска поставщиков
            query = """
                SELECT supplier_id, supplier_name, contact_person, phone_number, email
                FROM suppliers
                WHERE supplier_name ILIKE %s 
                   OR contact_person ILIKE %s 
                   OR phone_number LIKE %s
                   OR email ILIKE %s
                ORDER BY supplier_name
            """
            # Параметр поиска
            search_param = f"%{search_text}%"
            # Выполнение поиска
            suppliers = self.db.fetch_all(query, (search_param, search_param, search_param, search_param))

            # Установка количества строк в таблице
            self.suppliers_table.setRowCount(len(suppliers))

            # Заполнение таблицы результатами поиска
            for row_idx, supplier in enumerate(suppliers):
                for col_idx, data in enumerate(supplier):
                    item = QTableWidgetItem(str(data) if data else "")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.suppliers_table.setItem(row_idx, col_idx, item)
                    
            # Обновление счетчика для результатов поиска
            self.supplier_count_label.setText(f"Найдено поставщиков: {len(suppliers)}")
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка поиска поставщиков: {str(e)}")

    def add_supplier(self):
        """Отображение диалога добавления нового поставщика"""
        # Создание диалога добавления поставщика
        dialog = AddSupplierDialog(self, self.db)
        if dialog.exec():
            # Получение данных поставщика из диалога
            supplier_data = dialog.get_supplier_data()
            try:
                # SQL-запрос для добавления поставщика
                query = """
                    INSERT INTO suppliers (supplier_name, contact_person, phone_number, email)
                    VALUES (%s, %s, %s, %s)
                """
                # Параметры запроса
                params = (
                    supplier_data["name"],
                    supplier_data["contact"],
                    supplier_data["phone"],
                    supplier_data["email"]
                )
                # Выполнение запроса
                success = self.db.execute_query(query, params)
                if success:
                    # Обновление списка поставщиков
                    self.load_suppliers()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Поставщик успешно добавлен")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось добавить поставщика")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка добавления поставщика: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить поставщика: {str(e)}")

    def delete_supplier(self):
        """Удаление выбранного поставщика"""
        # Получение выбранных строк
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если поставщик не выбран
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для удаления")
            return

        # Получение номера строки и ID поставщика
        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()
        # Получение названия поставщика
        supplier_name = self.suppliers_table.item(row, 1).text()

        # Проверка наличия связанных заказов
        try:
            # SQL-запрос для проверки связанных заказов
            check_query = "SELECT COUNT(*) FROM orders WHERE supplier_id = %s"
            count = self.db.fetch_one(check_query, (supplier_id,))
            
            if count and count[0] > 0:
                # Отображение предупреждения о наличии связанных заказов
                QMessageBox.warning(
                    self, 
                    "Внимание", 
                    f"Поставщик '{supplier_name}' имеет связанные заказы и не может быть удален."
                )
                return
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка проверки заказов поставщика: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось проверить связанные заказы: {str(e)}")
            return

        # Создание диалога подтверждения
        confirm_dialog = ConfirmDialog(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить поставщика:\n{supplier_name}?"
        )
        
        if confirm_dialog.exec():
            try:
                # SQL-запрос для удаления поставщика
                query = "DELETE FROM suppliers WHERE supplier_id = %s"
                # Выполнение запроса
                success = self.db.execute_query(query, (supplier_id,))
                if success:
                    # Обновление списка поставщиков
                    self.load_suppliers()
                    # Отображение сообщения об успехе
                    QMessageBox.information(self, "Успех", "Поставщик успешно удален")
                else:
                    # Отображение сообщения об ошибке
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить поставщика")
            except Exception as e:
                # Логирование ошибки
                logging.error(f"Ошибка удаления поставщика: {str(e)}")
                # Отображение сообщения об ошибке
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить поставщика: {str(e)}")

    def edit_supplier(self):
        """Редактирование выбранного поставщика"""
        # Получение выбранных строк
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если поставщик не выбран
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для редактирования")
            return

        # Получение номера строки и ID поставщика
        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()

        try:
            # SQL-запрос для получения данных поставщика
            query = """
                SELECT supplier_name, contact_person, phone_number, email 
                FROM suppliers 
                WHERE supplier_id = %s
            """
            # Получение данных поставщика
            supplier = self.db.fetch_one(query, (supplier_id,))
            
            if supplier:
                # Создание диалога редактирования
                dialog = AddSupplierDialog(self, self.db)
                dialog.setWindowTitle("Редактировать поставщика")
                
                # Заполнение полей диалога текущими данными
                dialog.name_input.setText(supplier[0] if supplier[0] else "")
                dialog.contact_input.setText(supplier[1] if supplier[1] else "")
                dialog.phone_input.setText(supplier[2] if supplier[2] else "")
                dialog.email_input.setText(supplier[3] if supplier[3] else "")

                if dialog.exec():
                    # Получение обновленных данных
                    updated_data = dialog.get_supplier_data()
                    # SQL-запрос для обновления поставщика
                    update_query = """
                        UPDATE suppliers 
                        SET supplier_name = %s, 
                            contact_person = %s, 
                            phone_number = %s, 
                            email = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE supplier_id = %s
                    """
                    # Параметры запроса
                    update_params = (
                        updated_data["name"],
                        updated_data["contact"],
                        updated_data["phone"],
                        updated_data["email"],
                        supplier_id
                    )
                    # Выполнение запроса
                    success = self.db.execute_query(update_query, update_params)
                    if success:
                        # Обновление списка поставщиков
                        self.load_suppliers()
                        # Отображение сообщения об успехе
                        QMessageBox.information(self, "Успех", "Данные поставщика успешно обновлены")
                    else:
                        # Отображение сообщения об ошибке
                        QMessageBox.warning(self, "Ошибка", "Не удалось обновить данные поставщика")
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка редактирования поставщика: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось редактировать поставщика: {str(e)}")

    def send_email(self):
        """Отправка письма выбранному поставщику"""
        # Получение выбранных строк
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если поставщик не выбран
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для отправки письма")
            return

        # Получение данных о поставщике
        row = selected_rows[0].row()
        supplier_name = self.suppliers_table.item(row, 1).text()
        email = self.suppliers_table.item(row, 4).text()
        
        if not email:
            # Отображение предупреждения, если email не указан
            QMessageBox.warning(self, "Внимание", "У выбранного поставщика не указан email")
            return
            
        # Создание диалога отправки письма
        dialog = EmailDialog(self)
        # Заполнение полей диалога
        dialog.to_input.setText(email)
        dialog.subject_input.setText(f"Запрос от компании \"WareHouse\"")
        
        if dialog.exec():
            # В реальном приложении здесь была бы отправка письма
            QMessageBox.information(self, "Отправка письма", f"Письмо для {supplier_name} успешно отправлено")

    def show_supplier_orders(self):
        """Отображение заказов выбранного поставщика"""
        # Получение выбранных строк
        selected_rows = self.suppliers_table.selectedItems()
        if not selected_rows:
            # Отображение предупреждения, если поставщик не выбран
            QMessageBox.warning(self, "Внимание", "Выберите поставщика для просмотра заказов")
            return

        # Получение данных о поставщике
        row = selected_rows[0].row()
        supplier_id = self.suppliers_table.item(row, 0).text()
        supplier_name = self.suppliers_table.item(row, 1).text()
        
        try:
            # SQL-запрос для получения заказов поставщика
            query = """
                SELECT order_id, order_date, total_amount, status
                FROM orders
                WHERE supplier_id = %s
                ORDER BY order_date DESC
            """
            # Получение списка заказов
            orders = self.db.fetch_all(query, (supplier_id,))
            
            if not orders:
                # Отображение сообщения, если заказов нет
                QMessageBox.information(self, "Заказы поставщика", f"У поставщика {supplier_name} нет заказов")
                return
                
            # Форматирование текста с информацией о заказах
            details_text = f"Заказы поставщика: {supplier_name}\n\n"
            details_text += "ID | Дата | Сумма | Статус\n"
            details_text += "--------------------------------\n"
            
            # Добавление информации о каждом заказе
            for order in orders:
                details_text += f"{order[0]} | {order[1]} | {order[2]}₽ | {order[3]}\n"
                
            # Отображение информации о заказах
            QMessageBox.information(self, "Заказы поставщика", details_text)
            
        except Exception as e:
            # Логирование ошибки
            logging.error(f"Ошибка отображения заказов поставщика: {str(e)}")
            # Отображение сообщения об ошибке
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы поставщика: {str(e)}")

    def export_data(self):
        """Экспорт данных о поставщиках"""
        # Простая реализация - в реальном приложении использовалась бы функциональность экспорта
        QMessageBox.information(self, "Экспорт", "Функция экспорта пока не реализована") 