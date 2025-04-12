from PyQt6.QtWidgets import QMainWindow, QTabWidget, QStatusBar
from database import Database
from tabs.products_tab import ProductsTab
from tabs.stock_tab import StockTab
from tabs.orders_tab import OrdersTab
from tabs.suppliers_tab import SuppliersTab
from tabs.warehouses_tab import WarehousesTab
from styles import APP_STYLESHEET

class WarehouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.set_styles()

    def set_styles(self):
        self.setStyleSheet(APP_STYLESHEET)

    def init_ui(self):
        self.setWindowTitle("Система управления складом")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_tabs()
        self.setup_status_bar()

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs for different sections
        self.products_tab = ProductsTab(self.db)
        self.stock_tab = StockTab(self.db)
        self.orders_tab = OrdersTab(self.db)
        self.suppliers_tab = SuppliersTab(self.db)
        self.warehouses_tab = WarehousesTab(self.db)

        # Add tabs to tab widget
        self.tabs.addTab(self.products_tab, "Товары")
        self.tabs.addTab(self.stock_tab, "Запасы")
        self.tabs.addTab(self.orders_tab, "Заказы")
        self.tabs.addTab(self.suppliers_tab, "Поставщики")
        self.tabs.addTab(self.warehouses_tab, "Склады")

    def set_user_info(self, full_name: str, is_admin: bool):
        self.full_name = full_name
        self.is_admin = is_admin
        self.status_bar.showMessage(f"Вы вошли как: {full_name} | {'Администратор' if is_admin else 'Менеджер'}")
        
        # Update tab access based on user role
        if not is_admin:
            # If not admin, disable certain tabs or features
            pass 