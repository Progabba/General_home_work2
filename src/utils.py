from datetime import datetime

def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени суток"""
    current_time = datetime.now()
    hour = current_time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

# Пример использования функции
print(get_greeting())
