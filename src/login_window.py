from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QCheckBox, QHBoxLayout, QDialog, QFormLayout
)
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor, QLinearGradient, QBrush, QPalette
from PyQt6.QtCore import Qt, pyqtSignal, QSettings
from auth_service import AuthService
import os
import logging

class LoginWindow(QWidget):
    login_success = pyqtSignal(str, bool)  # full_name, is_admin

    def __init__(self):
        super().__init__()
        self.settings = QSettings("WarehouseSystem", "Auth")
        self.setWindowTitle("Система управления складом - Вход")
        self.setFixedSize(500, 600)
        self.setup_background()
        self.setup_ui()
        self.load_saved_credentials()

    def setup_background(self):
        """Setup static background"""
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#e8f5e9"))
        gradient.setColorAt(1, QColor("#a5d6a7"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def setup_ui(self):
        """Setup user interface"""
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Logo
        self.logo = QLabel()
        self.logo.setText("СКЛАД")
        self.logo.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.logo.setStyleSheet("color: #2e7d32;")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel("Авторизация")
        self.title.setStyleSheet("""
            QLabel {
                color: #2e7d32;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        self.username_input.setClearButtonEnabled(True)
        self.username_input.setStyleSheet(self.get_input_style())

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.setStyleSheet(self.get_input_style())

        # "Remember me" checkbox
        self.remember_check = QCheckBox("Запомнить меня")
        self.remember_check.setStyleSheet("""
            QCheckBox {
                color: #2e7d32;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)

        # Login button
        self.login_btn = QPushButton("Войти")
        self.login_btn.setStyleSheet(self.get_button_style("#2e7d32", "#43a047", "#1b5e20"))

        # "Forgot password" button
        self.forgot_btn = QPushButton("Забыли пароль?")
        self.forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2e7d32;
                text-decoration: underline;
                font-size: 12px;
                min-width: 0;
                padding: 0;
            }
            QPushButton:hover {
                color: #43a047;
            }
        """)

        # Footer
        self.footer = QLabel("© 2025 Система управления складом. Все права защищены.")
        self.footer.setStyleSheet("color: #888; font-size: 12px;")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Assemble UI
        main_layout.addStretch(1)
        main_layout.addWidget(self.logo)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)

        # Horizontal layout for checkbox and password recovery button
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.remember_check)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.forgot_btn)
        main_layout.addLayout(bottom_layout)

        main_layout.addWidget(self.login_btn)
        main_layout.addStretch(2)
        main_layout.addWidget(self.footer)

        self.setLayout(main_layout)

        # Connect signals
        self.login_btn.clicked.connect(self.check_credentials)
        self.forgot_btn.clicked.connect(self.show_password_recovery_dialog)

    def get_input_style(self):
        return """
            QLineEdit {
                background-color: rgba(255,255,255,0.9);
                border: 2px solid #a5d6a7;
                border-radius: 15px;
                padding: 12px;
                font-size: 16px;
                min-width: 280px;
                selection-background-color: #81c784;
            }
            QLineEdit:focus {
                border: 2px solid #2e7d32;
                background-color: white;
            }
        """

    def get_button_style(self, normal, hover, pressed):
        return f"""
            QPushButton {{
                background-color: {normal};
                color: white;
                border-radius: 15px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
                min-width: 280px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """

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

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Изменение пароля")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #a5d6a7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2e7d32;
            }
        """)
        form_layout.addRow("Логин:", self.username_input)
        
        # Current password input
        self.current_password = QLineEdit()
        self.current_password.setPlaceholderText("Введите текущий пароль")
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #a5d6a7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2e7d32;
            }
        """)
        form_layout.addRow("Текущий пароль:", self.current_password)
        
        # New password input
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Введите новый пароль")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #a5d6a7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2e7d32;
            }
        """)
        form_layout.addRow("Новый пароль:", self.new_password)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Cancel button
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        # Submit button
        self.submit_btn = QPushButton("Изменить пароль")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #43a047;
            }
        """)
        
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.submit_btn)
        
        # Add all layouts to main layout
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        self.resize(400, 300)
        
        # Connect signals
        self.cancel_btn.clicked.connect(self.reject)
        self.submit_btn.clicked.connect(self.change_password)
    
    def change_password(self):
        username = self.username_input.text()
        current_password = self.current_password.text()
        new_password = self.new_password.text()
        
        if not username or not current_password or not new_password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return
        
        if current_password == new_password:
            QMessageBox.warning(self, "Ошибка", "Новый пароль не должен совпадать с текущим")
            return
        
        success = AuthService.change_password(username, current_password, new_password)
        
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось изменить пароль. Проверьте введенные данные.") 