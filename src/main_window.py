"""
Модуль основного окна приложения для управления складом.

Этот модуль содержит класс WarehouseApp, который представляет собой
главное окно приложения с вкладками для различных функций системы.

:author: Игорь Валуйсков
:version: 1.0
"""
# Импорт необходимых виджетов из PyQt6
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QMenuBar, QMenu, QMessageBox
# Импорт класса для управления основным циклом приложения
from PyQt6.QtCore import QCoreApplication
# Импорт класса для работы с базой данных
from database import Database
# Импорт классов для вкладок с разделами приложения
from tabs.products_tab import ProductsTab
from tabs.stock_tab import StockTab
from tabs.orders_tab import OrdersTab
from tabs.suppliers_tab import SuppliersTab
from tabs.warehouses_tab import WarehousesTab
# Импорт стилей приложения
from styles import APP_STYLESHEET
from visualization import InventoryAnalysisDialog, OrdersReportDialog
from data_export import DataExporter, DataImporter

# Основной класс приложения, наследующий от QMainWindow
class WarehouseApp(QMainWindow):
    """
    Основной класс приложения для управления складом.
    
    Представляет собой главное окно приложения с вкладками для различных
    функций системы, включая работу с товарами, запасами, заказами,
    поставщиками и складами.
    """
    # Конструктор класса
    def __init__(self):
        """
        Инициализация основного окна приложения.
        
        Создает экземпляр класса базы данных и инициализирует
        пользовательский интерфейс.
        """
        # Вызов конструктора родительского класса
        super().__init__()
        # Создание объекта базы данных
        self.db = Database()
        # Инициализация пользовательского интерфейса
        self.init_ui()
        # Применение стилей к интерфейсу
        self.set_styles()

    # Метод для применения стилей к приложению
    def set_styles(self):
        """
        Применение стилей к приложению.
        
        Устанавливает таблицу стилей для всех элементов интерфейса.
        
        :returns: None
        """
        # Установка таблицы стилей для всего приложения
        self.setStyleSheet(APP_STYLESHEET)

    # Метод инициализации пользовательского интерфейса
    def init_ui(self):
        """
        Инициализация элементов пользовательского интерфейса.
        
        Устанавливает заголовок, размеры окна, настраивает меню,
        вкладки и строку состояния.
        
        :returns: None
        """
        # Установка заголовка главного окна
        self.setWindowTitle("Система управления складом")
        # Установка позиции и размеров окна (x, y, ширина, высота)
        self.setGeometry(100, 100, 1200, 800)
        # Настройка меню приложения
        self.setup_menu_bar()
        # Настройка вкладок приложения
        self.setup_tabs()
        # Настройка строки состояния
        self.setup_status_bar()

    # Метод настройки меню приложения
    def setup_menu_bar(self):
        """
        Настройка меню приложения.
        
        Создает панель меню с различными пунктами и подменю:
        - Файл (импорт/экспорт, выход)
        - Отчеты
        - Справка
        
        :returns: None
        """
        # Создание панели меню
        menu_bar = QMenuBar(self)
        # Установка панели меню в главное окно
        self.setMenuBar(menu_bar)
        
        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        
        # Добавляем подменю для импорта/экспорта
        import_export_menu = QMenu("Импорт/Экспорт", self)
        file_menu.addMenu(import_export_menu)
        
        # Действия для импорта
        import_csv_action = import_export_menu.addAction("Импорт из CSV")
        import_csv_action.triggered.connect(self.import_from_csv)
        
        import_excel_action = import_export_menu.addAction("Импорт из Excel")
        import_excel_action.triggered.connect(self.import_from_excel)
        
        # Разделитель
        import_export_menu.addSeparator()
        
        # Действия для экспорта
        export_csv_action = import_export_menu.addAction("Экспорт в CSV")
        export_csv_action.triggered.connect(self.export_to_csv)
        
        export_excel_action = import_export_menu.addAction("Экспорт в Excel")
        export_excel_action.triggered.connect(self.export_to_excel)
        
        # Разделитель в основном меню
        file_menu.addSeparator()
        
        # Действие "Выход"
        exit_action = file_menu.addAction("Выход")
        exit_action.triggered.connect(QCoreApplication.quit)
        
        # Меню "Отчеты"
        reports_menu = menu_bar.addMenu("Отчеты")
        
        # Действия для отчетов
        inventory_report_action = reports_menu.addAction("Анализ запасов")
        inventory_report_action.triggered.connect(self.show_inventory_analysis)
        
        sales_report_action = reports_menu.addAction("Отчеты по заказам")
        sales_report_action.triggered.connect(self.show_sales_report)
        
        # Меню "Справка"
        help_menu = menu_bar.addMenu("Справка")
        
        # Действие "О программе"
        about_action = help_menu.addAction("О программе")
        about_action.triggered.connect(self.show_about_dialog)
    
    # Метод отображения диалога "О программе"
    def show_about_dialog(self):
        """
        Отображение диалога "О программе".
        
        Показывает информационное окно с названием и описанием приложения.
        
        :returns: None
        """
        # Показать диалоговое окно "О программе"
        QMessageBox.about(
            self,  # Родительское окно
            "О программе",  # Заголовок диалога
            "Система управления складом v1.0\n\nРазработано для управления складскими операциями, товарами и поставщиками."  # Текст сообщения
        )

    # Метод настройки строки состояния
    def setup_status_bar(self):
        """
        Настройка строки состояния.
        
        Создает и инициализирует строку состояния в нижней части окна.
        
        :returns: None
        """
        # Создание строки состояния
        self.status_bar = QStatusBar()
        # Установка строки состояния в главное окно
        self.setStatusBar(self.status_bar)
        # Отображение начального сообщения "Готово" в строке состояния
        self.status_bar.showMessage("Готово")

    # Метод настройки вкладок
    def setup_tabs(self):
        """
        Настройка вкладок приложения.
        
        Создает виджет вкладок и добавляет основные разделы приложения:
        товары, запасы, заказы, поставщики, склады.
        
        :returns: None
        """
        # Создание виджета вкладок
        self.tabs = QTabWidget()
        # Установка виджета вкладок как центрального виджета
        self.setCentralWidget(self.tabs)

        # Создание вкладок для различных разделов
        # Создание вкладки товаров с передачей объекта базы данных
        self.products_tab = ProductsTab(self.db)
        # Создание вкладки запасов с передачей объекта базы данных
        self.stock_tab = StockTab(self.db)
        # Создание вкладки заказов с передачей объекта базы данных
        self.orders_tab = OrdersTab(self.db)
        # Создание вкладки поставщиков с передачей объекта базы данных
        self.suppliers_tab = SuppliersTab(self.db)
        # Создание вкладки складов с передачей объекта базы данных
        self.warehouses_tab = WarehousesTab(self.db)

        # Добавление вкладок в виджет вкладок
        # Добавление вкладки товаров с названием
        self.tabs.addTab(self.products_tab, "Товары")
        # Добавление вкладки запасов с названием
        self.tabs.addTab(self.stock_tab, "Запасы")
        # Добавление вкладки заказов с названием
        self.tabs.addTab(self.orders_tab, "Заказы")
        # Добавление вкладки поставщиков с названием
        self.tabs.addTab(self.suppliers_tab, "Поставщики")
        # Добавление вкладки складов с названием
        self.tabs.addTab(self.warehouses_tab, "Склады")

    # Метод установки информации о пользователе
    def set_user_info(self, full_name: str, is_admin: bool):
        """
        Установка информации о пользователе.
        
        :param full_name: Полное имя пользователя
        :type full_name: str
        :param is_admin: Флаг администратора
        :type is_admin: bool
        
        :returns: None
        """
        # Сохранение полного имени пользователя
        self.full_name = full_name
        # Сохранение информации о правах администратора
        self.is_admin = is_admin
        # Отображение информации о пользователе в строке состояния
        self.status_bar.showMessage(f"Вы вошли как: {full_name} | {'Администратор' if is_admin else 'Менеджер'}")
        
        # Обновление доступа к вкладкам на основе роли пользователя
        if not is_admin:
            # Если не администратор, отключить определенные вкладки или функции
            self.tabs.setTabEnabled(4, False)  # Отключаем вкладку "Склады"

    def import_from_csv(self):
        """
        Импорт данных из CSV файла.
        
        Определяет текущую активную вкладку и вызывает
        соответствующий метод импорта данных.
        
        :returns: None
        """
        current_tab_index = self.tabs.currentIndex()
        table_name = ""
        
        # Определяем таблицу на основе текущей вкладки
        if current_tab_index == 0:  # Товары
            table_name = "products"
        # elif current_tab_index == 1:  # Запасы
        #     table_name = "stock"
        # elif current_tab_index == 2:  # Заказы
        #     table_name = "orders"
        elif current_tab_index == 3:  # Поставщики
            table_name = "suppliers"
        elif current_tab_index == 4:  # Склады
            table_name = "warehouses"
        
        if table_name:
            importer = DataImporter(self)
            importer.import_from_csv(table_name)
            
            # Обновляем данные на текущей вкладке
            self.refresh_current_tab()
        else:
            QMessageBox.warning(self, "Импорт данных", "Импорт данных не поддерживается для этой вкладки")
    
    def import_from_excel(self):
        """
        Импорт данных из Excel файла.
        
        Определяет текущую активную вкладку и вызывает
        соответствующий метод импорта данных.
        
        :returns: None
        """
        current_tab_index = self.tabs.currentIndex()
        table_name = ""
        
        # Определяем таблицу на основе текущей вкладки
        if current_tab_index == 0:  # Товары
            table_name = "products"
        # elif current_tab_index == 1:  # Запасы
        #     table_name = "stock"
        # elif current_tab_index == 2:  # Заказы
        #     table_name = "orders"
        elif current_tab_index == 3:  # Поставщики
            table_name = "suppliers"
        elif current_tab_index == 4:  # Склады
            table_name = "warehouses"
        
        if table_name:
            importer = DataImporter(self)
            importer.import_from_excel(table_name)
            
            # Обновляем данные на текущей вкладке
            self.refresh_current_tab()
        else:
            QMessageBox.warning(self, "Импорт данных", "Импорт данных не поддерживается для этой вкладки")
    
    def export_to_csv(self):
        """
        Экспорт данных в CSV файл.
        
        Определяет текущую активную вкладку и формирует соответствующий
        SQL-запрос и заголовки для экспорта данных.
        
        :returns: None
        """
        # Получение индекса текущей активной вкладки
        current_tab_index = self.tabs.currentIndex()
        # Инициализация переменных для SQL-запроса и заголовков
        query = ""
        headers = []
        
        # Определение SQL-запроса и заголовков в зависимости от текущей вкладки
        if current_tab_index == 0:  # Вкладка "Товары"
            # Запрос для получения информации о товарах
            query = """
                SELECT product_name, product_description, category, unit_price
                FROM products
                ORDER BY product_name
            """
            # Заголовки для CSV файла
            headers = ["Название", "Описание", "Категория", "Цена"]
        elif current_tab_index == 1:  # Вкладка "Запасы"
            # Запрос для получения информации о запасах
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, s.last_restocked
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                ORDER BY p.product_name
            """
            # Заголовки для CSV файла
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение"]
        elif current_tab_index == 2:  # Вкладка "Заказы"
            # Запрос для получения информации о заказах
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, o.status
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                ORDER BY o.order_date DESC
            """
            # Заголовки для CSV файла
            headers = ["ID", "Дата", "Поставщик", "Сумма", "Статус"]
        elif current_tab_index == 3:  # Вкладка "Поставщики"
            # Запрос для получения информации о поставщиках
            query = """
                SELECT supplier_name, contact_person, phone_number, email
                FROM suppliers
                ORDER BY supplier_name
            """
            # Заголовки для CSV файла
            headers = ["Название", "Контактное лицо", "Телефон", "Email"]
        elif current_tab_index == 4:  # Вкладка "Склады"
            # Запрос для получения информации о складах
            query = """
                SELECT warehouse_name, location, capacity
                FROM warehouses
                ORDER BY warehouse_name
            """
            # Заголовки для CSV файла
            headers = ["Название", "Местоположение", "Вместимость"]
        
        # Если запрос определен, выполняем экспорт
        if query:
            # Создание объекта для экспорта данных
            exporter = DataExporter(self)
            # Вызов метода экспорта в CSV
            exporter.export_to_csv(query, headers=headers)
        else:
            # Показать сообщение об ошибке, если не удалось определить данные для экспорта
            QMessageBox.warning(self, "Экспорт данных", "Не удалось определить данные для экспорта")
    
    def export_to_excel(self):
        """
        Экспорт данных в Excel файл.
        
        Определяет текущую активную вкладку и формирует соответствующий
        SQL-запрос, заголовки и имя листа для экспорта данных.
        
        :returns: None
        """
        # Получение индекса текущей активной вкладки
        current_tab_index = self.tabs.currentIndex()
        # Инициализация переменных для SQL-запроса, заголовков и имени листа
        query = ""
        headers = []
        sheet_name = "Данные"
        
        # Определение SQL-запроса, заголовков и имени листа в зависимости от текущей вкладки
        if current_tab_index == 0:  # Вкладка "Товары"
            # Запрос для получения информации о товарах
            query = """
                SELECT product_name, product_description, category, unit_price
                FROM products
                ORDER BY product_name
            """
            # Заголовки для Excel файла
            headers = ["Название", "Описание", "Категория", "Цена"]
            # Имя листа в Excel
            sheet_name = "Товары"
        elif current_tab_index == 1:  # Вкладка "Запасы"
            # Запрос для получения информации о запасах
            query = """
                SELECT p.product_name, w.warehouse_name, s.quantity, s.last_restocked
                FROM stock s
                JOIN products p ON s.product_id = p.product_id
                JOIN warehouses w ON s.warehouse_id = w.warehouse_id
                ORDER BY p.product_name
            """
            # Заголовки для Excel файла
            headers = ["Товар", "Склад", "Количество", "Последнее пополнение"]
            # Имя листа в Excel
            sheet_name = "Запасы"
        elif current_tab_index == 2:  # Вкладка "Заказы"
            # Запрос для получения информации о заказах
            query = """
                SELECT o.order_id, o.order_date, s.supplier_name, o.total_amount, o.status
                FROM orders o
                JOIN suppliers s ON o.supplier_id = s.supplier_id
                ORDER BY o.order_date DESC
            """
            # Заголовки для Excel файла
            headers = ["ID", "Дата", "Поставщик", "Сумма", "Статус"]
            # Имя листа в Excel
            sheet_name = "Заказы"
        elif current_tab_index == 3:  # Вкладка "Поставщики"
            # Запрос для получения информации о поставщиках
            query = """
                SELECT supplier_name, contact_person, phone_number, email
                FROM suppliers
                ORDER BY supplier_name
            """
            # Заголовки для Excel файла
            headers = ["Название", "Контактное лицо", "Телефон", "Email"]
            # Имя листа в Excel
            sheet_name = "Поставщики"
        elif current_tab_index == 4:  # Вкладка "Склады"
            # Запрос для получения информации о складах
            query = """
                SELECT warehouse_name, location, capacity
                FROM warehouses
                ORDER BY warehouse_name
            """
            # Заголовки для Excel файла
            headers = ["Название", "Местоположение", "Вместимость"]
            # Имя листа в Excel
            sheet_name = "Склады"
        
        # Если запрос определен, выполняем экспорт
        if query:
            # Создание объекта для экспорта данных
            exporter = DataExporter(self)
            # Вызов метода экспорта в Excel
            exporter.export_to_excel(query, headers=headers, sheet_name=sheet_name)
        else:
            # Показать сообщение об ошибке, если не удалось определить данные для экспорта
            QMessageBox.warning(self, "Экспорт данных", "Не удалось определить данные для экспорта")
    
    def show_inventory_analysis(self):
        """
        Показать диалог анализа запасов.
        
        Создает и отображает диалоговое окно для анализа данных о запасах.
        
        :returns: None
        """
        # Создание и отображение диалога анализа запасов
        dialog = InventoryAnalysisDialog(self)
        dialog.exec()
    
    def show_sales_report(self):
        """
        Показать диалог отчетов по заказам.
        
        Создает и отображает диалоговое окно с отчетами по заказам.
        
        :returns: None
        """
        # Создание и отображение диалога отчетов по продажам
        dialog = OrdersReportDialog(self)
        dialog.exec()
    
    def refresh_current_tab(self):
        """
        Обновить данные на текущей вкладке.
        
        Определяет активную вкладку и вызывает соответствующий метод
        для обновления отображаемых данных.
        
        :returns: None
        """
        # Получение индекса текущей активной вкладки
        current_tab_index = self.tabs.currentIndex()
        
        # Обновление данных в зависимости от текущей вкладки
        if current_tab_index == 0:  # Вкладка "Товары"
            # Загрузка списка товаров
            self.products_tab.load_products()
        elif current_tab_index == 1:  # Вкладка "Запасы"
            # Загрузка информации о запасах
            self.stock_tab.load_stock()
        elif current_tab_index == 2:  # Вкладка "Заказы"
            # Загрузка списка заказов
            self.orders_tab.load_orders()
        elif current_tab_index == 3:  # Вкладка "Поставщики"
            # Загрузка списка поставщиков
            self.suppliers_tab.load_suppliers()
        elif current_tab_index == 4:  # Вкладка "Склады"
            # Загрузка списка складов
            self.warehouses_tab.load_warehouses() 