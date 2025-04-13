"""
This file contains the styling definitions for the Warehouse Management System
"""

# Main application stylesheet
APP_STYLESHEET = """
/* Global styles */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    color: #e0e0e0;
    background-color: #1e1e1e;
}

/* Main window */
QMainWindow {
    background-color: #1e1e1e;
}

/* Menu bar */
QMenuBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 2px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 12px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #3d3d3d;
}

QMenu {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
}

QMenu::item {
    padding: 6px 15px;
}

QMenu::item:selected {
    background-color: #3d3d3d;
    color: #ffffff;
}

/* Status bar */
QStatusBar {
    background-color: #2d2d2d;
    color: #7ab0df;
    border-top: 1px solid #3d3d3d;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background-color: #2d2d2d;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 8px 15px;
    border: 1px solid #3d3d3d;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #3d3d3d;
    border-bottom: none;
    padding-bottom: 10px;
    font-weight: bold;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* Buttons */
QPushButton {
    background-color: #0078d7;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #1a88e0;
}

QPushButton:pressed {
    background-color: #00639c;
}

QPushButton:disabled {
    background-color: #4d4d4d;
    color: #808080;
}

/* Secondary buttons */
QPushButton[secondary="true"] {
    background-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #505050;
}

QPushButton[secondary="true"]:hover {
    background-color: #505050;
}

QPushButton[secondary="true"]:pressed {
    background-color: #2d2d2d;
}

/* Danger buttons */
QPushButton[danger="true"] {
    background-color: #c42b1c;
}

QPushButton[danger="true"]:hover {
    background-color: #d9362b;
}

QPushButton[danger="true"]:pressed {
    background-color: #a81b0d;
}

/* Table widget */
QTableWidget {
    alternate-background-color: #252525;
    gridline-color: #3d3d3d;
    selection-background-color: #0078d7;
    selection-color: white;
    border: 1px solid #3d3d3d;
    background-color: #1e1e1e;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #0078d7;
    color: white;
}

QHeaderView::section {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 6px;
    border: 1px solid #3d3d3d;
    font-weight: bold;
}

/* Line edit */
QLineEdit {
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QLineEdit:focus {
    border: 1px solid #0078d7;
    background-color: #2d2d2d;
}

/* Combo box */
QComboBox {
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QComboBox:focus {
    border: 1px solid #0078d7;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 15px;
    border-left: none;
}

QComboBox::down-arrow {
    image: url(dropdown-arrow.png);
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    selection-background-color: #0078d7;
    selection-color: white;
}

/* Spin box */
QSpinBox, QDoubleSpinBox {
    padding: 8px;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #0078d7;
}

/* Checkbox */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    border: 1px solid #3d3d3d;
    background-color: #2d2d2d;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #0078d7;
    border: 1px solid #0078d7;
    border-radius: 3px;
}

/* Radio button */
QRadioButton {
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
}

QRadioButton::indicator:unchecked {
    border: 1px solid #3d3d3d;
    background-color: #2d2d2d;
    border-radius: 9px;
}

QRadioButton::indicator:checked {
    background-color: #2e7d32;
    border: 1px solid #2e7d32;
    border-radius: 10px;
}

/* Group box */
QGroupBox {
    border: 1px solid #c8e6c9;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    color: #2e7d32;
    padding: 0 5px;
    background-color: #f5f5f5;
}

/* Progress bar */
QProgressBar {
    border: 1px solid #c8e6c9;
    border-radius: 4px;
    text-align: center;
    background-color: #f5f5f5;
}

QProgressBar::chunk {
    background-color: #2e7d32;
    width: 10px;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background-color: #f5f5f5;
    width: 12px;
    margin: 12px 0 12px 0;
}

QScrollBar::handle:vertical {
    background-color: #a5d6a7;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #81c784;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 12px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #f5f5f5;
    height: 12px;
    margin: 0 12px 0 12px;
}

QScrollBar::handle:horizontal {
    background-color: #a5d6a7;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #81c784;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 12px;
}

/* Calendar widget */
QCalendarWidget QToolButton {
    color: #e0e0e0;
    background-color: transparent;
}

QCalendarWidget QMenu {
    width: 150px;
    left: 20px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #2d2d2d;
    padding: 2px;
}

QCalendarWidget QWidget#qt_calendar_prevmonth,
QCalendarWidget QWidget#qt_calendar_nextmonth {
    qproperty-icon: url(arrow.png);
    padding: 2px;
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #0078d7;
    selection-color: white;
}

"""

# Dialog box styles
DIALOG_STYLESHEET = """
QDialog {
    background-color: #1e1e1e;
    border: 1px solid #3d3d3d;
}

QDialog QLabel {
    font-size: 13px;
    color: #e0e0e0;
}

QDialog QLabel[title="true"] {
    font-size: 16px;
    font-weight: bold;
    color: #7ab0df;
}

QDialog QPushButton {
    min-width: 100px;
}
"""

# Login window stylesheet
LOGIN_STYLESHEET = """
/* Login window background */
#loginWidget {
    background-color: #1e1e1e;
}

/* Login logo and title */
#loginLogo {
    color: #7ab0df;
    font-size: 32px;
    font-weight: bold;
}

#loginTitle {
    color: #7ab0df;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Login input fields */
#loginInput {
    background-color: #2d2d2d;
    border: 2px solid #3d3d3d;
    border-radius: 15px;
    padding: 12px;
    font-size: 16px;
    min-width: 280px;
    color: #e0e0e0;
    selection-background-color: #0078d7;
}

#loginInput:focus {
    border: 2px solid #0078d7;
    background-color: #2d2d2d;
}

/* Login checkbox */
#rememberCheck {
    color: #e0e0e0;
    font-size: 14px;
}

#rememberCheck::indicator {
    width: 16px;
    height: 16px;
}

#rememberCheck::indicator:unchecked {
    border: 1px solid #3d3d3d;
    background-color: #2d2d2d;
    border-radius: 3px;
}

#rememberCheck::indicator:checked {
    background-color: #0078d7;
    border: 1px solid #0078d7;
    border-radius: 3px;
}

/* Login button */
#loginButton {
    background-color: #0078d7;
    color: white;
    border-radius: 15px;
    padding: 14px;
    font-size: 16px;
    font-weight: bold;
    min-width: 280px;
    border: none;
}

#loginButton:hover {
    background-color: #1a88e0;
}

#loginButton:pressed {
    background-color: #00639c;
}

/* Forgot password button */
#forgotButton {
    background: transparent;
    color: #7ab0df;
    text-decoration: underline;
    font-size: 12px;
    min-width: 0;
    padding: 0;
}

#forgotButton:hover {
    color: #0078d7;
}

/* Footer */
#loginFooter {
    color: #808080;
    font-size: 12px;
}

/* Password Recovery Dialog */
#recoveryTitle {
    color: #7ab0df;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
}

#recoveryInput {
    padding: 10px;
    border: 1px solid #3d3d3d;
    border-radius: 5px;
    font-size: 14px;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

#recoveryInput:focus {
    border: 1px solid #0078d7;
}

#recoveryFormLabel {
    color: #e0e0e0;
    font-size: 14px;
}
"""