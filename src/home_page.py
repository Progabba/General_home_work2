from datetime import datetime
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import json
import requests

def load_excel_to_dataframe(file_name: str) -> DataFrame:
    """Функция читает эксель файл и возвращает дата фрейм"""
    df = pd.read_excel(file_name)
    return df


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


def get_card_summary(df: pd.DataFrame) -> list:
    """Возвращает информацию по каждой карте: последние 4 цифры, общая сумма расходов, кешбэк"""
    card_summary = []  # Создаем пустой список для хранения информации по картам
    for card in df['Номер карты'].unique():  # Перебираем уникальные значения из столбца 'Номер карты'
        print(f"Обработка карты: {card}")
        card_df = df[df['Номер карты'] == card]  # Фильтруем датафрейм по текущей карте
        print(card_df)
        total_spent = card_df['Сумма платежа'].sum()  # Считаем общую сумму расходов для текущей карты
        print(total_spent)
        cashback = total_spent / 100  # Рассчитываем кешбэк как 1% от общей суммы расходов
        # Добавляем информацию по текущей карте в список card_summary
        card_summary.append({
            'last_digits': str(card)[-4:],  # Последние 4 цифры номера карты
            'total_spent': round(total_spent, 2),  # Общая сумма расходов
            'cashback': round(cashback, 2)  # Кешбэк
        })
    return card_summary




if __name__ == '__main__':
    # Пример использования функции
    print(get_greeting())

    operations = load_excel_to_dataframe('operations.xls')

    print(get_card_summary(operations))
