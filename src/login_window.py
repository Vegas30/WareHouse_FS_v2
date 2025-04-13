from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QCheckBox, QHBoxLayout, QDialog, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QSettings
from auth_service import AuthService
from styles import LOGIN_STYLESHEET
import os
import logging

class LoginWindow(QWidget):
    login_success = pyqtSignal(str, bool)  # Сигнал успешной авторизации (передает имя пользователя и права администратора)

    def __init__(self):
        super().__init__()
        self.settings = QSettings("WarehouseSystem", "Auth")
        self.setWindowTitle("Система управления складом - Вход")
        self.setFixedSize(500, 600)
        self.setObjectName("loginWidget")
        self.setup_ui()
        self.setStyleSheet(LOGIN_STYLESHEET)
        self.load_saved_credentials()

    def setup_ui(self):
        """Setup user interface"""
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Logo - Создание и настройка логотипа
        self.logo = QLabel()
        self.logo.setText("СКЛАД")
        self.logo.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.logo.setObjectName("loginLogo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title - Создание и настройка заголовка
        self.title = QLabel("Авторизация")
        self.title.setObjectName("loginTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input fields - Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setClearButtonEnabled(True)
        self.username_input.setObjectName("loginInput")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setObjectName("loginInput")

        # "Remember me" checkbox - Флажок "Запомнить меня"
        self.remember_check = QCheckBox("Запомнить меня")
        self.remember_check.setObjectName("rememberCheck")

        # Login button - Кнопка входа
        self.login_btn = QPushButton("Войти")
        self.login_btn.setObjectName("loginButton")

        # "Forgot password" button - Кнопка "Забыли пароль?"
        self.forgot_btn = QPushButton("Забыли пароль?")
        self.forgot_btn.setObjectName("forgotButton")

        # Footer - Нижний колонтитул
        self.footer = QLabel("© 2025 Система управления складом. Все права защищены.")
        self.footer.setObjectName("loginFooter")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Assemble UI - Сборка интерфейса
        main_layout.addStretch(1)
        main_layout.addWidget(self.logo)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)

        # Horizontal layout for checkbox and password recovery button - Горизонтальный макет для флажка и кнопки восстановления
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.remember_check)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.forgot_btn)
        main_layout.addLayout(bottom_layout)

        main_layout.addWidget(self.login_btn)
        main_layout.addStretch(2)
        main_layout.addWidget(self.footer)

        self.setLayout(main_layout)

        # Connect signals - Подключение сигналов
        self.login_btn.clicked.connect(self.check_credentials)
        self.forgot_btn.clicked.connect(self.show_password_recovery_dialog)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        success, full_name, is_admin = AuthService.authenticate(username, password)

        if success:
            if self.remember_check.isChecked():
                self.save_credentials(username, password)
            else:
                self.clear_credentials()

            self.login_success.emit(full_name, is_admin)
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def show_password_recovery_dialog(self):
        dialog = PasswordRecoveryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Успех", "Пароль успешно изменен!")

    def save_credentials(self, username, password):
        self.settings.setValue("username", username)
        self.settings.setValue("password", password)
        self.settings.setValue("remember", True)

    def clear_credentials(self):
        self.settings.remove("username")
        self.settings.remove("password")
        self.settings.setValue("remember", False)

    def load_saved_credentials(self):
        if self.settings.value("remember", False, type=bool):
            username = self.settings.value("username", "", type=str)
            password = self.settings.value("password", "", type=str)
            self.username_input.setText(username)
            self.password_input.setText(password)
            self.remember_check.setChecked(True)


class PasswordRecoveryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Восстановление пароля")
        self.setup_ui()
        self.setStyleSheet(LOGIN_STYLESHEET)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title - Заголовок
        title = QLabel("Изменение пароля")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setObjectName("recoveryTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form layout for inputs - Макет формы для полей ввода
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        # Username input - Поле ввода логина
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setObjectName("recoveryInput")
        
        # Create form labels with styles - Создание меток формы со стилями
        username_label = QLabel("Логин:")
        username_label.setObjectName("recoveryFormLabel")
        
        # Current password input - Поле ввода текущего пароля
        self.current_password = QLineEdit()
        self.current_password.setPlaceholderText("Введите текущий пароль")
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setObjectName("recoveryInput")
        
        current_password_label = QLabel("Текущий пароль:")
        current_password_label.setObjectName("recoveryFormLabel")
        
        # New password input - Поле ввода нового пароля
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Введите новый пароль")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setObjectName("recoveryInput")
        
        new_password_label = QLabel("Новый пароль:")
        new_password_label.setObjectName("recoveryFormLabel")
        
        # Add to form layout - Добавление элементов в макет формы
        form_layout.addRow(username_label, self.username_input)
        form_layout.addRow(current_password_label, self.current_password)
        form_layout.addRow(new_password_label, self.new_password)
        
        # Button layout - Макет для кнопок
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        # Cancel button - Кнопка отмены
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setObjectName("loginButton")
        
        # Submit button - Кнопка подтверждения
        self.submit_btn = QPushButton("Изменить пароль")
        self.submit_btn.setObjectName("loginButton")
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.submit_btn)
        
        # Add layouts to main layout - Добавление макетов в основной макет
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Connect signals - Подключение сигналов
        self.cancel_btn.clicked.connect(self.reject)
        self.submit_btn.clicked.connect(self.change_password)
        
    def change_password(self):
        username = self.username_input.text()
        current_password = self.current_password.text()
        new_password = self.new_password.text()
        
        if not username or not current_password or not new_password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
            
        # Validate current password and change to new password - Проверка текущего пароля и изменение на новый
        if AuthService.change_password(username, current_password, new_password):
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль") 