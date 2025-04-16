"""
This file contains the styling definitions for the Warehouse Management System
"""

# Main application stylesheet
APP_STYLESHEET = """
/* Глобальные стили для всех виджетов */
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif; /* Шрифт по умолчанию */
    font-size: 12px; /* Размер шрифта */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    background-color: #1e1e1e; /* Цвет фона (RGB: 30, 30, 30) - темно-серый */
}

/* Стили для главного окна */
QMainWindow {
    background-color: #1e1e1e; /* Цвет фона главного окна (RGB: 30, 30, 30) - темно-серый */
}

/* Стили для строки меню */
QMenuBar {
    background-color: #2d2d2d; /* Цвет фона строки меню (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста в строке меню (RGB: 224, 224, 224) - светло-серый */
    padding: 2px; /* Внутренние отступы */
}

/* Стили для элементов строки меню */
QMenuBar::item {
    background-color: transparent; /* Прозрачный фон */
    padding: 4px 12px; /* Внутренние отступы */
    border-radius: 4px; /* Скругление углов */
}

/* Стили для выбранного элемента строки меню */
QMenuBar::item:selected {
    background-color: #3d3d3d; /* Цвет фона при выборе (RGB: 61, 61, 61) - серый */
}

/* Стили для выпадающего меню */
QMenu {
    background-color: #2d2d2d; /* Цвет фона меню (RGB: 45, 45, 45) - темно-серый */
    border: 1px solid #3d3d3d; /* Граница меню (RGB: 61, 61, 61) - серый */
}

/* Стили для элементов выпадающего меню */
QMenu::item {
    padding: 6px 15px; /* Внутренние отступы */
}

/* Стили для выбранного элемента выпадающего меню */
QMenu::item:selected {
    background-color: #3d3d3d; /* Цвет фона при выборе (RGB: 61, 61, 61) - серый */
    color: #ffffff; /* Цвет текста при выборе (RGB: 255, 255, 255) - белый */
}

/* Стили для строки состояния */
QStatusBar {
    background-color: #2d2d2d; /* Цвет фона строки состояния (RGB: 45, 45, 45) - темно-серый */
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
    border-top: 1px solid #3d3d3d; /* Верхняя граница (RGB: 61, 61, 61) - серый */
}

/* Стили для панели вкладок */
QTabWidget::pane {
    border: 1px solid #3d3d3d; /* Граница панели (RGB: 61, 61, 61) - серый */
    background-color: #2d2d2d; /* Цвет фона панели (RGB: 45, 45, 45) - темно-серый */
}

/* Стили для вкладок */
QTabBar::tab {
    background-color: #2d2d2d; /* Цвет фона вкладки (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    padding: 8px 15px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница вкладки (RGB: 61, 61, 61) - серый */
    border-bottom: none; /* Убираем нижнюю границу */
    border-top-left-radius: 4px; /* Скругление верхнего левого угла */
    border-top-right-radius: 4px; /* Скругление верхнего правого угла */
}

/* Стили для выбранной вкладки */
QTabBar::tab:selected {
    background-color: #3d3d3d; /* Цвет фона при выборе (RGB: 61, 61, 61) - серый */
    border-bottom: none; /* Убираем нижнюю границу */
    padding-bottom: 10px; /* Увеличиваем нижний отступ */
    font-weight: bold; /* Жирный шрифт */
}

/* Стили для невыбранных вкладок */
QTabBar::tab:!selected {
    margin-top: 2px; /* Верхний отступ */
}

/* Стили для кнопок */
QPushButton {
    background-color: #0078d7; /* Цвет фона кнопки (RGB: 0, 120, 215) - синий */
    color: white; /* Цвет текста (RGB: 255, 255, 255) - белый */
    border: none; /* Убираем границу */
    padding: 8px 16px; /* Внутренние отступы */
    border-radius: 4px; /* Скругление углов */
    min-width: 80px; /* Минимальная ширина */
}

/* Стили для кнопки при наведении */
QPushButton:hover {
    background-color: #1a88e0; /* Цвет фона при наведении (RGB: 26, 136, 224) - светло-синий */
}

/* Стили для нажатой кнопки */
QPushButton:pressed {
    background-color: #00639c; /* Цвет фона при нажатии (RGB: 0, 99, 156) - темно-синий */
}

/* Стили для отключенной кнопки */
QPushButton:disabled {
    background-color: #4d4d4d; /* Цвет фона отключенной кнопки (RGB: 77, 77, 77) - серый */
    color: #808080; /* Цвет текста отключенной кнопки (RGB: 128, 128, 128) - серый */
}

/* Стили для вторичных кнопок */
QPushButton[secondary="true"] {
    background-color: #3d3d3d; /* Цвет фона вторичной кнопки (RGB: 61, 61, 61) - серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    border: 1px solid #505050; /* Граница (RGB: 80, 80, 80) - серый */
}

/* Стили для вторичной кнопки при наведении */
QPushButton[secondary="true"]:hover {
    background-color: #505050; /* Цвет фона при наведении (RGB: 80, 80, 80) - серый */
}

/* Стили для нажатой вторичной кнопки */
QPushButton[secondary="true"]:pressed {
    background-color: #2d2d2d; /* Цвет фона при нажатии (RGB: 45, 45, 45) - темно-серый */
}

/* Стили для опасных кнопок */
QPushButton[danger="true"] {
    background-color: #c42b1c; /* Цвет фона опасной кнопки (RGB: 196, 43, 28) - красный */
}

/* Стили для опасной кнопки при наведении */
QPushButton[danger="true"]:hover {
    background-color: #d9362b; /* Цвет фона при наведении (RGB: 217, 54, 43) - светло-красный */
}

/* Стили для нажатой опасной кнопки */
QPushButton[danger="true"]:pressed {
    background-color: #a81b0d; /* Цвет фона при нажатии (RGB: 168, 27, 13) - темно-красный */
}

/* Стили для таблицы */
QTableWidget {
    alternate-background-color: #252525; /* Цвет фона чередующихся строк (RGB: 37, 37, 37) - темно-серый */
    gridline-color: #3d3d3d; /* Цвет линий сетки (RGB: 61, 61, 61) - серый */
    selection-background-color: #0078d7; /* Цвет фона выделения (RGB: 0, 120, 215) - синий */
    selection-color: white; /* Цвет текста выделения (RGB: 255, 255, 255) - белый */
    border: 1px solid #3d3d3d; /* Граница таблицы (RGB: 61, 61, 61) - серый */
    background-color: #1e1e1e; /* Цвет фона таблицы (RGB: 30, 30, 30) - темно-серый */
}

/* Стили для ячеек таблицы */
QTableWidget::item {
    padding: 5px; /* Внутренние отступы */
}

/* Стили для выбранной ячейки таблицы */
QTableWidget::item:selected {
    background-color: #0078d7; /* Цвет фона при выборе (RGB: 0, 120, 215) - синий */
    color: white; /* Цвет текста при выборе (RGB: 255, 255, 255) - белый */
}

/* Стили для заголовков таблицы */
QHeaderView::section {
    background-color: #2d2d2d; /* Цвет фона заголовка (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    padding: 6px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    font-weight: bold; /* Жирный шрифт */
}

/* Стили для поля ввода */
QLineEdit {
    padding: 8px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    border-radius: 4px; /* Скругление углов */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
}

/* Стили для поля ввода при фокусе */
QLineEdit:focus {
    border: 1px solid #0078d7; /* Цвет границы при фокусе (RGB: 0, 120, 215) - синий */
    background-color: #2d2d2d; /* Цвет фона при фокусе (RGB: 45, 45, 45) - темно-серый */
}

/* Стили для выпадающего списка */
QComboBox {
    padding: 8px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    border-radius: 4px; /* Скругление углов */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
}

/* Стили для выпадающего списка при фокусе */
QComboBox:focus {
    border: 1px solid #0078d7; /* Цвет границы при фокусе (RGB: 0, 120, 215) - синий */
}

/* Стили для кнопки выпадающего списка */
QComboBox::drop-down {
    subcontrol-origin: padding; /* Позиционирование */
    subcontrol-position: center right; /* Позиция */
    width: 15px; /* Ширина */
    border-left: none; /* Убираем левую границу */
}

/* Стили для стрелки выпадающего списка */
QComboBox::down-arrow {
    image: url(dropdown-arrow.png); /* Изображение стрелки */
}

/* Стили для выпадающего меню списка */
QComboBox QAbstractItemView {
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    selection-background-color: #0078d7; /* Цвет фона выделения (RGB: 0, 120, 215) - синий */
    selection-color: white; /* Цвет текста выделения (RGB: 255, 255, 255) - белый */
}

/* Стили для числового поля ввода */
QSpinBox, QDoubleSpinBox {
    padding: 8px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    border-radius: 4px; /* Скругление углов */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
}

/* Стили для числового поля ввода при фокусе */
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #0078d7; /* Цвет границы при фокусе (RGB: 0, 120, 215) - синий */
}

/* Стили для флажка */
QCheckBox {
    spacing: 8px; /* Расстояние между флажком и текстом */
}

/* Стили для индикатора флажка */
QCheckBox::indicator {
    width: 18px; /* Ширина */
    height: 18px; /* Высота */
}

/* Стили для неотмеченного флажка */
QCheckBox::indicator:unchecked {
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    border-radius: 3px; /* Скругление углов */
}

/* Стили для отмеченного флажка */
QCheckBox::indicator:checked {
    background-color: #0078d7; /* Цвет фона (RGB: 0, 120, 215) - синий */
    border: 1px solid #0078d7; /* Граница (RGB: 0, 120, 215) - синий */
    border-radius: 3px; /* Скругление углов */
}

/* Стили для переключателя */
QRadioButton {
    spacing: 8px; /* Расстояние между переключателем и текстом */
}

/* Стили для индикатора переключателя */
QRadioButton::indicator {
    width: 18px; /* Ширина */
    height: 18px; /* Высота */
}

/* Стили для невыбранного переключателя */
QRadioButton::indicator:unchecked {
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    border-radius: 9px; /* Скругление углов */
}

/* Стили для выбранного переключателя */
QRadioButton::indicator:checked {
    background-color: #2e7d32; /* Цвет фона (RGB: 46, 125, 50) - зеленый */
    border: 1px solid #2e7d32; /* Граница (RGB: 46, 125, 50) - зеленый */
    border-radius: 10px; /* Скругление углов */
}

/* Стили для группы элементов */
QGroupBox {
    border: 1px solid #c8e6c9; /* Граница (RGB: 200, 230, 201) - светло-зеленый */
    border-radius: 6px; /* Скругление углов */
    margin-top: 12px; /* Верхний отступ */
    padding-top: 15px; /* Верхний внутренний отступ */
}

/* Стили для заголовка группы */
QGroupBox::title {
    subcontrol-origin: margin; /* Позиционирование */
    subcontrol-position: top left; /* Позиция */
    color: #2e7d32; /* Цвет текста (RGB: 46, 125, 50) - зеленый */
    padding: 0 5px; /* Внутренние отступы */
    background-color: #f5f5f5; /* Цвет фона (RGB: 245, 245, 245) - светло-серый */
}

/* Стили для индикатора прогресса */
QProgressBar {
    border: 1px solid #c8e6c9; /* Граница (RGB: 200, 230, 201) - светло-зеленый */
    border-radius: 4px; /* Скругление углов */
    text-align: center; /* Выравнивание текста */
    background-color: #f5f5f5; /* Цвет фона (RGB: 245, 245, 245) - светло-серый */
}

/* Стили для заполнения индикатора прогресса */
QProgressBar::chunk {
    background-color: #2e7d32; /* Цвет заполнения (RGB: 46, 125, 50) - зеленый */
    width: 10px; /* Ширина сегмента */
}

/* Стили для вертикальной полосы прокрутки */
QScrollBar:vertical {
    border: none; /* Убираем границу */
    background-color: #f5f5f5; /* Цвет фона (RGB: 245, 245, 245) - светло-серый */
    width: 12px; /* Ширина */
    margin: 12px 0 12px 0; /* Внешние отступы */
}

/* Стили для ползунка вертикальной полосы прокрутки */
QScrollBar::handle:vertical {
    background-color: #f5f5f5; /* Цвет ползунка (RGB: 165, 214, 167) - светло-зеленый */
    border-radius: 6px; /* Скругление углов */
    min-height: 20px; /* Минимальная высота */
}

/* Стили для ползунка вертикальной полосы прокрутки при наведении */
QScrollBar::handle:vertical:hover {
    background-color: #2d2d2d; /* Цвет при наведении (RGB: 129, 199, 132) - зеленый */
}

/* Стили для кнопок вертикальной полосы прокрутки */
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none; /* Убираем границу */
    background: none; /* Убираем фон */
    height: 12px; /* Высота */
}

/* Стили для горизонтальной полосы прокрутки */
QScrollBar:horizontal {
    border: none; /* Убираем границу */
    background-color: #f5f5f5; /* Цвет фона (RGB: 245, 245, 245) - светло-серый */
    height: 12px; /* Высота */
    margin: 0 12px 0 12px; /* Внешние отступы */
}

/* Стили для ползунка горизонтальной полосы прокрутки */
QScrollBar::handle:horizontal {
    background-color: #f5f5f5; /* Цвет ползунка (RGB: 165, 214, 167) - светло-зеленый */
    border-radius: 6px; /* Скругление углов */
    min-width: 20px; /* Минимальная ширина */
}

/* Стили для ползунка горизонтальной полосы прокрутки при наведении */
QScrollBar::handle:horizontal:hover {
    background-color: #2d2d2d; /* Цвет при наведении (RGB: 129, 199, 132) - зеленый */
}

/* Стили для кнопок горизонтальной полосы прокрутки */
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none; /* Убираем границу */
    background: none; /* Убираем фон */
    width: 12px; /* Ширина */
}

/* Стили для виджета календаря */
QCalendarWidget QToolButton {
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    background-color: transparent; /* Прозрачный фон */
}

/* Стили для меню календаря */
QCalendarWidget QMenu {
    width: 150px; /* Ширина */
    left: 20px; /* Отступ слева */
}

/* Стили для панели навигации календаря */
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    padding: 2px; /* Внутренние отступы */
}

/* Стили для кнопок навигации календаря */
QCalendarWidget QWidget#qt_calendar_prevmonth,
QCalendarWidget QWidget#qt_calendar_nextmonth {
    qproperty-icon: url(arrow.png); /* Изображение стрелки */
    padding: 2px; /* Внутренние отступы */
}

/* Стили для представления календаря */
QCalendarWidget QAbstractItemView {
    selection-background-color: #0078d7; /* Цвет фона выделения (RGB: 0, 120, 215) - синий */
    selection-color: white; /* Цвет текста выделения (RGB: 255, 255, 255) - белый */
}
"""

# Dialog box styles
DIALOG_STYLESHEET = """
/* Стили для диалогового окна */
QDialog {
    background-color: #1e1e1e; /* Цвет фона (RGB: 30, 30, 30) - темно-серый */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
}

/* Стили для меток в диалоговом окне */
QDialog QLabel {
    font-size: 13px; /* Размер шрифта */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
}

/* Стили для заголовков в диалоговом окне */
QDialog QLabel[title="true"] {
    font-size: 16px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
}

/* Стили для кнопок в диалоговом окне */
QDialog QPushButton {
    min-width: 100px; /* Минимальная ширина */
}
"""

# Login window stylesheet
LOGIN_STYLESHEET = """
/* Стили для фона окна входа */
#loginWidget {
    background-color: #1e1e1e; /* Цвет фона (RGB: 30, 30, 30) - темно-серый */
}

/* Стили для логотипа входа */
#loginLogo {
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
    font-size: 32px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
}

/* Стили для заголовка входа */
#loginTitle {
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
    font-size: 28px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
    margin-bottom: 20px; /* Нижний отступ */
}

/* Стили для полей ввода входа */
#loginInput {
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    border: 2px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    border-radius: 15px; /* Скругление углов */
    padding: 12px; /* Внутренние отступы */
    font-size: 16px; /* Размер шрифта */
    min-width: 280px; /* Минимальная ширина */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    selection-background-color: #0078d7; /* Цвет фона выделения (RGB: 0, 120, 215) - синий */
}

/* Стили для полей ввода входа при фокусе */
#loginInput:focus {
    border: 2px solid #0078d7; /* Цвет границы при фокусе (RGB: 0, 120, 215) - синий */
    background-color: #2d2d2d; /* Цвет фона при фокусе (RGB: 45, 45, 45) - темно-серый */
}

/* Стили для флажка "Запомнить" */
#rememberCheck {
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    font-size: 14px; /* Размер шрифта */
}

/* Стили для индикатора флажка "Запомнить" */
#rememberCheck::indicator {
    width: 16px; /* Ширина */
    height: 16px; /* Высота */
}

/* Стили для неотмеченного флажка "Запомнить" */
#rememberCheck::indicator:unchecked {
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    border-radius: 3px; /* Скругление углов */
}

/* Стили для отмеченного флажка "Запомнить" */
#rememberCheck::indicator:checked {
    background-color: #0078d7; /* Цвет фона (RGB: 0, 120, 215) - синий */
    border: 1px solid #0078d7; /* Граница (RGB: 0, 120, 215) - синий */
    border-radius: 3px; /* Скругление углов */
}

/* Стили для кнопки входа */
#loginButton {
    background-color: #0078d7; /* Цвет фона (RGB: 0, 120, 215) - синий */
    color: white; /* Цвет текста (RGB: 255, 255, 255) - белый */
    border-radius: 15px; /* Скругление углов */
    padding: 14px; /* Внутренние отступы */
    font-size: 16px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
    min-width: 280px; /* Минимальная ширина */
    border: none; /* Убираем границу */
}

/* Стили для кнопки входа при наведении */
#loginButton:hover {
    background-color: #1a88e0; /* Цвет фона при наведении (RGB: 26, 136, 224) - светло-синий */
}

/* Стили для нажатой кнопки входа */
#loginButton:pressed {
    background-color: #00639c; /* Цвет фона при нажатии (RGB: 0, 99, 156) - темно-синий */
}

/* Стили для кнопки "Забыли пароль" */
#forgotButton {
    background: transparent; /* Прозрачный фон */
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
    text-decoration: underline; /* Подчеркивание */
    font-size: 12px; /* Размер шрифта */
    min-width: 0; /* Минимальная ширина */
    padding: 0; /* Внутренние отступы */
}

/* Стили для кнопки "Забыли пароль" при наведении */
#forgotButton:hover {
    color: #0078d7; /* Цвет текста при наведении (RGB: 0, 120, 215) - синий */
}

/* Стили для нижнего колонтитула входа */
#loginFooter {
    color: #808080; /* Цвет текста (RGB: 128, 128, 128) - серый */
    font-size: 12px; /* Размер шрифта */
}

/* Стили для заголовка восстановления пароля */
#recoveryTitle {
    color: #7ab0df; /* Цвет текста (RGB: 122, 176, 223) - голубой */
    font-size: 16px; /* Размер шрифта */
    font-weight: bold; /* Жирный шрифт */
    margin-bottom: 10px; /* Нижний отступ */
}

/* Стили для поля ввода восстановления пароля */
#recoveryInput {
    padding: 10px; /* Внутренние отступы */
    border: 1px solid #3d3d3d; /* Граница (RGB: 61, 61, 61) - серый */
    border-radius: 5px; /* Скругление углов */
    font-size: 14px; /* Размер шрифта */
    background-color: #2d2d2d; /* Цвет фона (RGB: 45, 45, 45) - темно-серый */
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
}

/* Стили для поля ввода восстановления пароля при фокусе */
#recoveryInput:focus {
    border: 1px solid #0078d7; /* Цвет границы при фокусе (RGB: 0, 120, 215) - синий */
}

/* Стили для метки формы восстановления */
#recoveryFormLabel {
    color: #e0e0e0; /* Цвет текста (RGB: 224, 224, 224) - светло-серый */
    font-size: 14px; /* Размер шрифта */
}
"""