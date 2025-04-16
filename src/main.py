# Импорт системного модуля
import sys
# Импорт модуля для работы с операционной системой
import os

# Добавление текущей директории в путь поиска модулей
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Импорт необходимых компонентов из PyQt6
from PyQt6.QtWidgets import QApplication
# Импорт основного окна приложения
from main_window import WarehouseApp
# Импорт окна авторизации
from login_window import LoginWindow
# Импорт модуля для логирования
import logging

# Настройка логирования
log_path = os.path.join(os.path.dirname(current_dir), 'app.log')
logging.basicConfig(
    # Указание файла для записи логов
    filename=log_path,
    # Установка уровня логирования
    level=logging.DEBUG,
    # Формат записи логов
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # Создание экземпляра приложения
    app = QApplication(sys.argv)

    # Создание окон авторизации и основного приложения
    login_window = LoginWindow()
    main_window = WarehouseApp()

    # Обработчик успешной авторизации
    def handle_login(full_name: str, is_admin: bool):
        # Установка информации о пользователе
        main_window.set_user_info(full_name, is_admin)
        # Отображение основного окна
        main_window.show()

    # Подключение сигнала успешной авторизации к обработчику
    login_window.login_success.connect(handle_login)
    
    # Отображение окна авторизации
    login_window.show()

    # Запуск цикла обработки событий приложения
    sys.exit(app.exec())

# Точка входа в приложение
if __name__ == "__main__":
    main() 