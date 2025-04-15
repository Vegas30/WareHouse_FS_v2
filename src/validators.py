# Импорт модуля для работы с регулярными выражениями
import re
# Импорт типов для аннотаций
from typing import Union, Tuple, Any, Dict
# Импорт модуля для экранирования HTML
import html

class Validator:
    """Класс для валидации и санитизации входных данных"""
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, max_length: int = 255) -> Tuple[bool, str]:
        """Валидация текстовых полей
        
        Args:
            text: Текст для проверки
            min_length: Минимальная длина
            max_length: Максимальная длина
            
        Returns:
            Tuple[bool, str]: (Прошла ли проверка, сообщение об ошибке)
        """
        # Проверка на пустое значение
        if not text:
            return False, "Поле не может быть пустым"
        # Проверка минимальной длины
        if len(text) < min_length:
            return False, f"Минимальная длина поля - {min_length} символов"
        # Проверка максимальной длины
        if len(text) > max_length:
            return False, f"Максимальная длина поля - {max_length} символов"
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Валидация email адреса
        
        Args:
            email: Email для проверки
            
        Returns:
            Tuple[bool, str]: (Прошла ли проверка, сообщение об ошибке)
        """
        # Проверка на пустое значение
        if not email:
            return False, "Email не может быть пустым"
        
        # Регулярное выражение для проверки формата email
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        # Проверка соответствия формату
        if not re.match(email_pattern, email):
            return False, "Неверный формат email"
        return True, ""
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Валидация телефонного номера
        
        Args:
            phone: Номер телефона для проверки
            
        Returns:
            Tuple[bool, str]: (Прошла ли проверка, сообщение об ошибке)
        """
        # Проверка на пустое значение
        if not phone:
            return False, "Номер телефона не может быть пустым"
        
        # Удаление всех нецифровых символов
        digits_only = re.sub(r'\D', '', phone)
        
        # Проверка длины номера
        if len(digits_only) != 11:
            return False, "Номер телефона должен содержать 11 цифр"
        return True, ""
    
    @staticmethod
    def validate_number(value: Union[str, int, float], 
                        min_value: float = None, 
                        max_value: float = None) -> Tuple[bool, str]:
        """Валидация числовых значений
        
        Args:
            value: Значение для проверки
            min_value: Минимальное допустимое значение
            max_value: Максимальное допустимое значение
            
        Returns:
            Tuple[bool, str]: (Прошла ли проверка, сообщение об ошибке)
        """
        try:
            # Преобразование значения в число
            num_value = float(value)
            
            # Проверка минимального значения
            if min_value is not None and num_value < min_value:
                return False, f"Значение должно быть не меньше {min_value}"
            
            # Проверка максимального значения
            if max_value is not None and num_value > max_value:
                return False, f"Значение должно быть не больше {max_value}"
                
            return True, ""
        except (ValueError, TypeError):
            # Обработка ошибок преобразования
            return False, "Введите корректное число"
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Санитизация входных данных для защиты от инъекций
        
        Args:
            value: Значение для санитизации
            
        Returns:
            str: Безопасное значение
        """
        # Проверка типа входных данных
        if not isinstance(value, str):
            return value
            
        # Экранирование HTML-специальных символов
        sanitized = html.escape(value)
        
        # Удаление потенциально опасных последовательностей SQL-инъекций
        sanitized = re.sub(r"(\s|;|--)", " ", sanitized)
        
        return sanitized
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Санитизация словаря с данными
        
        Args:
            data: Словарь для санитизации
            
        Returns:
            Dict[str, Any]: Словарь с безопасными значениями
        """
        # Создание нового словаря для безопасных значений
        result = {}
        # Обработка каждого элемента словаря
        for key, value in data.items():
            # Санитизация строковых значений
            if isinstance(value, str):
                result[key] = Validator.sanitize_input(value)
            # Рекурсивная санитизация вложенных словарей
            elif isinstance(value, dict):
                result[key] = Validator.sanitize_dict(value)
            # Сохранение остальных типов без изменений
            else:
                result[key] = value
        return result 