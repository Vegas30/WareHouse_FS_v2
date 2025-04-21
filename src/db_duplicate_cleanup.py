#!/usr/bin/env python3
"""
Скрипт для удаления дублирующихся записей в таблице stock

Этот скрипт выполняет SQL-запросы для идентификации и удаления 
дублирующихся записей в таблице stock напрямую из приложения.
"""

import sys
import os
import logging
from datetime import datetime

# Добавление текущей директории в путь поиска модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Импорт класса для работы с базой данных
from database import Database
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox, QMessageBox

class StockCleanupTool(QWidget):
    """
    Инструмент для очистки дублирующихся записей в таблице stock
    """
    def __init__(self):
        super().__init__()
        
        # Настройка логирования
        self.setup_logging()
        
        # Создание подключения к базе данных
        self.db = Database()
        
        # Инициализация интерфейса
        self.init_ui()
        
        # Загрузка информации о дубликатах
        self.load_duplicates_info()
    
    def setup_logging(self):
        """Настройка логирования"""
        log_dir = os.path.join(os.path.dirname(current_dir), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_filename = f"stock_cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_path = os.path.join(log_dir, log_filename)
        
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        logging.info("Запуск инструмента очистки дубликатов")
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Настройка окна
        self.setWindowTitle("Очистка дубликатов в таблице Stock")
        self.setGeometry(100, 100, 800, 600)
        
        # Создание основного макета
        layout = QVBoxLayout()
        
        # Создание информационной метки
        info_label = QLabel("Этот инструмент позволяет найти и удалить дублирующиеся записи в таблице stock")
        layout.addWidget(info_label)
        
        # Создание выпадающего списка действий
        self.action_combo = QComboBox()
        self.action_combo.addItem("Оставить запись с максимальным количеством", "max")
        self.action_combo.addItem("Объединить дубликаты (суммировать количество)", "sum")
        layout.addWidget(QLabel("Выберите действие с дубликатами:"))
        layout.addWidget(self.action_combo)
        
        # Создание области для вывода результатов
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(QLabel("Информация о дубликатах:"))
        layout.addWidget(self.results_area)
        
        # Создание кнопок
        self.btn_refresh = QPushButton("Обновить информацию")
        self.btn_refresh.clicked.connect(self.load_duplicates_info)
        layout.addWidget(self.btn_refresh)
        
        self.btn_cleanup = QPushButton("Выполнить очистку")
        self.btn_cleanup.clicked.connect(self.cleanup_duplicates)
        layout.addWidget(self.btn_cleanup)
        
        self.btn_add_constraint = QPushButton("Добавить ограничение уникальности")
        self.btn_add_constraint.clicked.connect(self.add_unique_constraint)
        layout.addWidget(self.btn_add_constraint)
        
        # Установка макета
        self.setLayout(layout)
    
    def load_duplicates_info(self):
        """Загрузка информации о дубликатах"""
        try:
            # Очистка области вывода
            self.results_area.clear()
            
            # Запрос для идентификации дубликатов
            identification_query = """
                SELECT product_id, warehouse_id, COUNT(*) as duplicate_count
                FROM stock
                GROUP BY product_id, warehouse_id
                HAVING COUNT(*) > 1
                ORDER BY duplicate_count DESC;
            """
            
            # Выполнение запроса
            duplicates = self.db.fetch_all(identification_query, parent_widget=self)
            
            if not duplicates:
                self.results_area.append("Дубликаты не найдены! Таблица stock не содержит повторяющихся записей.")
                self.btn_cleanup.setEnabled(False)
                return
            
            # Вывод информации о количестве дубликатов
            self.results_area.append(f"Найдено {len(duplicates)} групп дублирующихся записей:\n")
            for product_id, warehouse_id, count in duplicates:
                # Получение имени товара
                product_query = "SELECT product_name FROM products WHERE product_id = %s"
                product_name = self.db.fetch_one(product_query, (product_id,), parent_widget=self)[0]
                
                # Получение названия склада
                warehouse_query = "SELECT warehouse_name FROM warehouses WHERE warehouse_id = %s"
                warehouse_name = self.db.fetch_one(warehouse_query, (warehouse_id,), parent_widget=self)[0]
                
                self.results_area.append(f"Товар: {product_name} | Склад: {warehouse_name} | Кол-во дубликатов: {count}")
                
                # Получение деталей о дубликатах
                details_query = """
                    SELECT stock_id, quantity, last_restocked
                    FROM stock
                    WHERE product_id = %s AND warehouse_id = %s
                    ORDER BY quantity DESC
                """
                details = self.db.fetch_all(details_query, (product_id, warehouse_id), parent_widget=self)
                
                for stock_id, quantity, last_restocked in details:
                    self.results_area.append(f"    ID: {stock_id}, Количество: {quantity}, Дата: {last_restocked}")
                
                self.results_area.append("")
            
            # Включение кнопки очистки
            self.btn_cleanup.setEnabled(True)
            
        except Exception as e:
            logging.error(f"Ошибка при загрузке информации о дубликатах: {str(e)}")
            self.results_area.append(f"Ошибка: {str(e)}")
            self.btn_cleanup.setEnabled(False)
    
    def cleanup_duplicates(self):
        """Очистка дубликатов в таблице stock"""
        try:
            # Получение выбранного действия
            action = self.action_combo.currentData()
            
            # Предупреждение перед выполнением
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Вы собираетесь удалить дублирующиеся записи в таблице stock.")
            msg_box.setInformativeText("Рекомендуется создать резервную копию базы данных перед выполнением операции. Продолжить?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            
            if msg_box.exec() != QMessageBox.StandardButton.Yes:
                return
            
            # Выбор запроса в зависимости от выбранного действия
            if action == "max":
                # Запрос для удаления дубликатов с сохранением одной записи с максимальным количеством
                query = """
                    -- Создаем временную таблицу для хранения уникальных записей
                    CREATE TEMPORARY TABLE temp_stock AS
                    SELECT DISTINCT ON (product_id, warehouse_id) 
                        stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
                    FROM stock
                    ORDER BY product_id, warehouse_id, quantity DESC;

                    -- Удаляем все записи из основной таблицы
                    DELETE FROM stock;

                    -- Вставляем уникальные записи обратно в основную таблицу
                    INSERT INTO stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at)
                    SELECT stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
                    FROM temp_stock;

                    -- Удаляем временную таблицу
                    DROP TABLE temp_stock;
                """
                operation_description = "с сохранением записей с максимальным количеством"
            else:  # action == "sum"
                # Запрос для объединения дубликатов (суммирование количества товаров)
                query = """
                    -- Создаем временную таблицу для хранения объединенных записей
                    CREATE TEMPORARY TABLE temp_stock AS
                    SELECT 
                        MIN(stock_id) as stock_id,
                        product_id,
                        warehouse_id,
                        SUM(quantity) as quantity,
                        MAX(last_restocked) as last_restocked,
                        MIN(created_at) as created_at,
                        MAX(updated_at) as updated_at
                    FROM stock
                    GROUP BY product_id, warehouse_id;

                    -- Удаляем все записи из основной таблицы
                    DELETE FROM stock;

                    -- Вставляем объединенные записи обратно в основную таблицу
                    INSERT INTO stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at)
                    SELECT stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
                    FROM temp_stock;

                    -- Удаляем временную таблицу
                    DROP TABLE temp_stock;
                """
                operation_description = "с суммированием количества товаров"
            
            # Выполнение запроса
            success = self.db.execute_query(query, parent_widget=self)
            
            if success:
                logging.info(f"Дубликаты успешно удалены {operation_description}")
                QMessageBox.information(self, "Успех", f"Дубликаты успешно удалены {operation_description}")
                
                # Обновление информации о дубликатах
                self.load_duplicates_info()
            else:
                logging.error("Не удалось удалить дубликаты")
                QMessageBox.critical(self, "Ошибка", "Не удалось удалить дубликаты")
            
        except Exception as e:
            logging.error(f"Ошибка при очистке дубликатов: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при очистке дубликатов: {str(e)}")
    
    def add_unique_constraint(self):
        """Добавление уникального ограничения для предотвращения будущих дубликатов"""
        try:
            # Предупреждение перед выполнением
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Вы собираетесь добавить ограничение уникальности для таблицы stock.")
            msg_box.setInformativeText("Это предотвратит появление дубликатов в будущем, но может вызвать ошибки, если дубликаты уже есть. Продолжить?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            
            if msg_box.exec() != QMessageBox.StandardButton.Yes:
                return
            
            # Проверка наличия дубликатов
            check_query = """
                SELECT COUNT(*) FROM (
                    SELECT product_id, warehouse_id
                    FROM stock
                    GROUP BY product_id, warehouse_id
                    HAVING COUNT(*) > 1
                ) as duplicates;
            """
            duplicate_count = self.db.fetch_one(check_query, parent_widget=self)[0]
            
            if duplicate_count > 0:
                QMessageBox.warning(
                    self, 
                    "Внимание", 
                    f"В таблице все еще есть {duplicate_count} групп дубликатов. "
                    "Сначала выполните очистку дубликатов."
                )
                return
            
            # Проверка существования ограничения
            check_constraint_query = """
                SELECT COUNT(*) FROM information_schema.table_constraints
                WHERE constraint_name = 'unique_product_warehouse'
                AND table_name = 'stock';
            """
            constraint_exists = self.db.fetch_one(check_constraint_query, parent_widget=self)[0] > 0
            
            if constraint_exists:
                QMessageBox.information(
                    self, 
                    "Информация", 
                    "Ограничение уникальности для таблицы stock уже существует."
                )
                return
            
            # Добавление ограничения
            query = """
                ALTER TABLE stock ADD CONSTRAINT unique_product_warehouse 
                UNIQUE (product_id, warehouse_id);
            """
            
            # Выполнение запроса
            success = self.db.execute_query(query, parent_widget=self)
            
            if success:
                logging.info("Ограничение уникальности успешно добавлено")
                QMessageBox.information(
                    self, 
                    "Успех", 
                    "Ограничение уникальности успешно добавлено. "
                    "Теперь в таблице stock не могут быть дублирующиеся записи для одного товара на одном складе."
                )
            else:
                logging.error("Не удалось добавить ограничение уникальности")
                QMessageBox.critical(self, "Ошибка", "Не удалось добавить ограничение уникальности")
            
        except Exception as e:
            logging.error(f"Ошибка при добавлении ограничения уникальности: {str(e)}")
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении ограничения уникальности: {str(e)}")


def main():
    """Основная функция для запуска инструмента"""
    app = QApplication(sys.argv)
    cleanup_tool = StockCleanupTool()
    cleanup_tool.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 