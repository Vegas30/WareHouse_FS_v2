# Импорт необходимых компонентов из PyQt6
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QCheckBox, QHBoxLayout, QDialog, QFormLayout
)
# Импорт компонентов для работы со шрифтами и графикой
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPalette, QBrush, QLinearGradient, QColor
# Импорт базовых компонентов Qt
from PyQt6.QtCore import Qt, pyqtSignal, QSettings
# Импорт сервиса авторизации
from auth_service import AuthService
# Импорт стилей
from styles import LOGIN_STYLESHEET, DIALOG_STYLESHEET
# Импорт модуля для работы с операционной системой
import os
# Импорт модуля для логирования
import logging

class LoginWindow(QWidget):
    # Сигнал успешной авторизации (передает имя пользователя и права администратора)
    login_success = pyqtSignal(str, bool)

    def __init__(self):
        # Инициализация родительского класса
        super().__init__()
        # Создание объекта для хранения настроек
        self.settings = QSettings("WarehouseSystem", "Auth")
        # Установка заголовка окна
        self.setWindowTitle("Система управления складом - Вход")
        # Установка фиксированного размера окна
        self.setFixedSize(500, 600)
        # Установка иконки окна
        self.setWindowIcon(QIcon("src/logo.png"))
        # Установка имени объекта для стилизации
        self.setObjectName("loginWidget")
        # Настройка фона
        self.setup_background()
        # Настройка пользовательского интерфейса
        self.setup_ui()
        # Применение стилей
        self.setStyleSheet(LOGIN_STYLESHEET)
        # Загрузка сохраненных учетных данных
        self.load_saved_credentials()

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание основного вертикального layout
        main_layout = QVBoxLayout()
        # Выравнивание по центру
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Установка отступов между элементами
        main_layout.setSpacing(15)
        # Установка отступов от краев
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Создание и настройка логотипа
        self.logo = QLabel()
        if os.path.exists("src/logo.png"):
            pixmap = QPixmap("src/logo.png")
            self.logo.setPixmap(pixmap.scaled(180, 180, 
                                              Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo.setText("СКЛАД")
            self.logo.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.logo.setObjectName("loginLogo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создание и настройка заголовка
        self.title = QLabel("Авторизация")
        self.title.setObjectName("loginTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создание и настройка полей ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setClearButtonEnabled(True)
        self.username_input.setObjectName("loginInput")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setObjectName("loginInput")

        # Создание и настройка флажка "Запомнить меня"
        self.remember_check = QCheckBox("Запомнить меня")
        self.remember_check.setObjectName("rememberCheck")

        # Создание и настройка кнопки входа
        self.login_btn = QPushButton("Войти")
        self.login_btn.setObjectName("loginButton")

        # Создание и настройка кнопки "Забыли пароль?"
        self.forgot_btn = QPushButton("Забыли пароль?")
        self.forgot_btn.setObjectName("forgotButton")

        # Создание и настройка нижнего колонтитула
        self.footer = QLabel("© 2025 Система управления складом. Все права защищены.")
        self.footer.setObjectName("loginFooter")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Сборка интерфейса
        main_layout.addStretch(1)
        main_layout.addWidget(self.logo)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)

        # Создание горизонтального layout для флажка и кнопки восстановления
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.remember_check)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.forgot_btn)
        main_layout.addLayout(bottom_layout)

        main_layout.addWidget(self.login_btn)
        main_layout.addStretch(2)
        main_layout.addWidget(self.footer)

        # Установка основного layout
        self.setLayout(main_layout)

        # Подключение обработчиков событий
        self.login_btn.clicked.connect(self.check_credentials)
        self.forgot_btn.clicked.connect(self.show_password_recovery_dialog)

    def check_credentials(self):
        # Получение введенных данных
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка на пустые поля
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        # Проверка учетных данных
        success, full_name, is_admin = AuthService.authenticate(username, password)

        if success:
            # Сохранение учетных данных, если установлен флажок
            if self.remember_check.isChecked():
                self.save_credentials(username, password)
            else:
                self.clear_credentials()

            # Отправка сигнала об успешной авторизации
            self.login_success.emit(full_name, is_admin)
            # Закрытие окна авторизации
            self.close()
        else:
            # Отображение сообщения об ошибке
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def show_password_recovery_dialog(self):
        # Создание и отображение диалога восстановления пароля
        dialog = PasswordRecoveryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Успех", "Пароль успешно изменен!")

    def save_credentials(self, username, password):
        # Сохранение учетных данных в настройках
        self.settings.setValue("username", username)
        self.settings.setValue("password", password)
        self.settings.setValue("remember", True)

    def clear_credentials(self):
        # Очистка сохраненных учетных данных
        self.settings.remove("username")
        self.settings.remove("password")
        self.settings.setValue("remember", False)

    def load_saved_credentials(self):
        # Загрузка сохраненных учетных данных
        if self.settings.value("remember", False, type=bool):
            username = self.settings.value("username", "", type=str)
            password = self.settings.value("password", "", type=str)
            self.username_input.setText(username)
            self.password_input.setText(password)
            self.remember_check.setChecked(True)

    def setup_background(self):
        """Настройка статического фона"""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#e7f0fd"))
        gradient.setColorAt(1, QColor("#accbee"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)


class PasswordRecoveryDialog(QDialog):
    def __init__(self, parent=None):
        # Инициализация родительского класса
        super().__init__(parent)
        # Установка заголовка окна
        self.setWindowTitle("Восстановление пароля")
        # Настройка пользовательского интерфейса
        self.setup_ui()
        # Применение стилей
        self.setStyleSheet(DIALOG_STYLESHEET + LOGIN_STYLESHEET)

    def setup_ui(self):
        # Создание основного вертикального layout
        layout = QVBoxLayout()
        # Установка отступов между элементами
        layout.setSpacing(20)
        
        # Создание и настройка заголовка
        title = QLabel("Изменение пароля")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setObjectName("recoveryTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Создание layout для формы
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        # Создание и настройка поля ввода логина
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setObjectName("recoveryInput")
        
        # Создание и настройка метки для логина
        username_label = QLabel("Логин:")
        username_label.setObjectName("recoveryFormLabel")
        
        # Создание и настройка поля ввода текущего пароля
        self.current_password = QLineEdit()
        self.current_password.setPlaceholderText("Введите текущий пароль")
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setObjectName("recoveryInput")
        
        # Создание и настройка метки для текущего пароля
        current_password_label = QLabel("Текущий пароль:")
        current_password_label.setObjectName("recoveryFormLabel")
        
        # Создание и настройка поля ввода нового пароля
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Введите новый пароль")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setObjectName("recoveryInput")
        
        # Создание и настройка метки для нового пароля
        new_password_label = QLabel("Новый пароль:")
        new_password_label.setObjectName("recoveryFormLabel")
        
        # Добавление элементов в layout формы
        form_layout.addRow(username_label, self.username_input)
        form_layout.addRow(current_password_label, self.current_password)
        form_layout.addRow(new_password_label, self.new_password)
        
        # Создание layout для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        # Создание и настройка кнопки отмены
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("loginButton")
        
        # Создание и настройка кнопки подтверждения
        self.submit_btn = QPushButton("Изменить пароль")
        self.submit_btn.setObjectName("loginButton")
        
        # Добавление кнопок в layout
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.submit_btn)
        
        # Добавление всех layout в основной layout
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        
        # Установка основного layout
        self.setLayout(layout)
        
        # Подключение обработчиков событий
        self.cancel_btn.clicked.connect(self.reject)
        self.submit_btn.clicked.connect(self.change_password)
        
    def change_password(self):
        # Получение введенных данных
        username = self.username_input.text()
        current_password = self.current_password.text()
        new_password = self.new_password.text()
        
        # Проверка на пустые поля
        if not username or not current_password or not new_password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        # Проверка текущего пароля и изменение на новый
        if AuthService.change_password(username, current_password, new_password):
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль") 