"""
This file contains the styling definitions for the Warehouse Management System
"""

# Main application stylesheet
APP_STYLESHEET = """
/* Global styles */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    color: #212121;
    background-color: #f5f5f5;
}

/* Main window */
QMainWindow {
    background-color: #f5f5f5;
}

/* Menu bar */
QMenuBar {
    background-color: #2e7d32;
    color: white;
    padding: 2px;
}

QMenuBar::item {
    background-color: transparent;
    padding: 4px 12px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #43a047;
}

QMenu {
    background-color: white;
    border: 1px solid #e0e0e0;
}

QMenu::item {
    padding: 6px 15px;
}

QMenu::item:selected {
    background-color: #e8f5e9;
    color: #2e7d32;
}

/* Status bar */
QStatusBar {
    background-color: #e8f5e9;
    color: #2e7d32;
    border-top: 1px solid #c8e6c9;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #c8e6c9;
    background-color: white;
}

QTabBar::tab {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 8px 15px;
    border: 1px solid #c8e6c9;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: none;
    padding-bottom: 10px;
    font-weight: bold;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* Buttons */
QPushButton {
    background-color: #2e7d32;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #43a047;
}

QPushButton:pressed {
    background-color: #1b5e20;
}

QPushButton:disabled {
    background-color: #9e9e9e;
    color: #e0e0e0;
}

/* Secondary buttons */
QPushButton[secondary="true"] {
    background-color: white;
    color: #2e7d32;
    border: 1px solid #2e7d32;
}

QPushButton[secondary="true"]:hover {
    background-color: #e8f5e9;
}

QPushButton[secondary="true"]:pressed {
    background-color: #c8e6c9;
}

/* Danger buttons */
QPushButton[danger="true"] {
    background-color: #d32f2f;
}

QPushButton[danger="true"]:hover {
    background-color: #f44336;
}

QPushButton[danger="true"]:pressed {
    background-color: #b71c1c;
}

/* Table widget */
QTableWidget {
    alternate-background-color: #f5f5f5;
    gridline-color: #e0e0e0;
    selection-background-color: #c8e6c9;
    selection-color: #212121;
    border: 1px solid #e0e0e0;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #c8e6c9;
    color: #212121;
}

QHeaderView::section {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 6px;
    border: 1px solid #c8e6c9;
    font-weight: bold;
}

/* Line edit */
QLineEdit {
    padding: 8px;
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border: 1px solid #2e7d32;
    background-color: #ffffff;
}

/* Combo box */
QComboBox {
    padding: 8px;
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    background-color: white;
}

QComboBox:focus {
    border: 1px solid #2e7d32;
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
    background-color: white;
    border: 1px solid #bdbdbd;
    selection-background-color: #c8e6c9;
    selection-color: #212121;
}

/* Spin box */
QSpinBox, QDoubleSpinBox {
    padding: 8px;
    border: 1px solid #bdbdbd;
    border-radius: 4px;
    background-color: white;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #2e7d32;
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
    border: 1px solid #bdbdbd;
    background-color: white;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #2e7d32;
    border: 1px solid #2e7d32;
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
    border: 1px solid #bdbdbd;
    background-color: white;
    border-radius: 10px;
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
    color: #2e7d32;
    background-color: transparent;
}

QCalendarWidget QMenu {
    width: 150px;
    left: 20px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #e8f5e9;
    padding: 2px;
}

QCalendarWidget QWidget#qt_calendar_prevmonth,
QCalendarWidget QWidget#qt_calendar_nextmonth {
    qproperty-icon: url(arrow.png);
    padding: 2px;
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #c8e6c9;
    selection-color: #212121;
}

"""

# Dialog box styles
DIALOG_STYLESHEET = """
QDialog {
    background-color: white;
    border: 1px solid #e0e0e0;
}

QDialog QLabel {
    font-size: 13px;
}

QDialog QLabel[title="true"] {
    font-size: 16px;
    font-weight: bold;
    color: #2e7d32;
}

QDialog QPushButton {
    min-width: 100px;
}
"""