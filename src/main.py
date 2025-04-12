import sys
import os
from PyQt6.QtWidgets import QApplication
from main_window import WarehouseApp
from login_window import LoginWindow
import logging

# Configure logging
logging.basicConfig(
    filename='../app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the login and main windows
    login_window = LoginWindow()
    main_window = WarehouseApp()

    # Handle successful login
    def handle_login(full_name: str, is_admin: bool):
        main_window.set_user_info(full_name, is_admin)
        main_window.show()

    # Connect the login success signal to the handle_login function
    login_window.login_success.connect(handle_login)
    
    # Show the login window
    login_window.show()

    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 