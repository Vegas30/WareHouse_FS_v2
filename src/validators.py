import re
from typing import Union, Tuple, Any, Dict
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
        if not text:
            return False, "Поле не может быть пустым"
        if len(text) < min_length:
            return False, f"Минимальная длина поля - {min_length} символов"
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
        if not email:
            return False, "Email не может быть пустым"
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
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
        if not phone:
            return False, "Номер телефона не может быть пустым"
        
        # Удаляем все нецифровые символы для проверки
        digits_only = re.sub(r'\D', '', phone)
        
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
            # Конвертируем в число
            num_value = float(value)
            
            if min_value is not None and num_value < min_value:
                return False, f"Значение должно быть не меньше {min_value}"
            
            if max_value is not None and num_value > max_value:
                return False, f"Значение должно быть не больше {max_value}"
                
            return True, ""
        except (ValueError, TypeError):
            return False, "Введите корректное число"
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """Санитизация входных данных для защиты от инъекций
        
        Args:
            value: Значение для санитизации
            
        Returns:
            str: Безопасное значение
        """
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
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = Validator.sanitize_input(value)
            elif isinstance(value, dict):
                result[key] = Validator.sanitize_dict(value)
            else:
                result[key] = value
        return result 