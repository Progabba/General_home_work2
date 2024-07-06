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
        #print(f"Обработка карты: {card}")
        card_df = df[df['Номер карты'] == card]  # Фильтруем датафрейм по текущей карте
        #print(card_df)
        total_spent = card_df['Сумма платежа'].sum()  # Считаем общую сумму расходов для текущей карты
        #print(total_spent)
        cashback = total_spent / 100  # Рассчитываем кешбэк как 1% от общей суммы расходов
        # Добавляем информацию по текущей карте в список card_summary
        card_summary.append({
            'last_digits': str(card)[-4:],  # Последние 4 цифры номера карты
            'total_spent': round(total_spent, 2),  # Общая сумма расходов
            'cashback': round(cashback, 2)  # Кешбэк
        })
    return card_summary

def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> list:
    """Возвращает топ-N транзакций по сумме платежа"""
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)  # Преобразуем столбец 'Дата операции' в datetime с dayfirst=True
    top_transactions = df.nlargest(top_n, 'Сумма платежа')
    top_transactions = top_transactions[['Дата операции', 'Сумма платежа', 'Категория', 'Описание']]
    top_transactions['Дата операции'] = top_transactions['Дата операции'].dt.strftime('%d.%m.%Y')
    formatted_transactions = []
    for index, row in top_transactions.iterrows():
        formatted_transactions.append({
            'date': row['Дата операции'],
            'amount': row['Сумма платежа'],
            'category': row['Категория'],
            'description': row['Описание']
        })
    return formatted_transactions

import requests

def get_currency_rates() -> list:
    url = 'https://api.exchangerate-api.com/v4/latest/RUB'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        usd_rate = 1 / data.get('rates', {}).get('USD')
        eur_rate = 1 / data.get('rates', {}).get('EUR')
        return [
            {'currency': 'USD', 'rate': usd_rate},
            {'currency': 'EUR', 'rate': eur_rate}
        ]
    return []



def get_stock_prices(api_key: str, symbols: list) -> list:
    """Возвращает стоимость акций для заданных символов (например, AAPL, AMZN)"""
    prices = []
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('Global Quote', {})
            prices.append({'stock': symbol, 'price': float(data.get('05. price', 0))})
    return prices


if __name__ == '__main__':
    # Пример использования функции
    print(get_greeting())

    operations = load_excel_to_dataframe('operations.xls')

    print(get_card_summary(operations))

    print(get_top_transactions(operations))

    print(get_currency_rates())

    api_key = 'LLFCICMLGVZP3MIE'
    symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    stock_prices = get_stock_prices(api_key, symbols)
    print(stock_prices)