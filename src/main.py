#ГЛАВНАЯ СТРАНИЦА
import json

from src.home_page import load_excel_to_dataframe, get_greeting, get_card_summary, get_top_transactions, \
    get_currency_rates, get_stock_prices


def main(file_name: str, api_key: str, stock_symbols: list) -> str:
    """Главная функция для создания JSON-ответа"""
    # Загрузка данных из Excel
    df = load_excel_to_dataframe(file_name)

    # Получение приветствия
    greeting = get_greeting()

    # Получение информации о картах
    card_summary = get_card_summary(df)

    # Получение топ-транзакций
    top_transactions = get_top_transactions(df)

    # Получение курсов валют
    currency_rates = get_currency_rates()

    # Получение цен акций
    stock_prices = get_stock_prices(api_key, stock_symbols)

    # Сбор всех данных в словарь
    data = {
        'greeting': greeting,
        'cards': card_summary,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }

    # Преобразование словаря в JSON
    json_data = json.dumps(data, ensure_ascii=False, indent=2)

    return json_data


# Пример использования
file_name = 'operations.xls'
api_key = 'LLFCICMLGVZP3MIE'
stock_symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
json_response = main(file_name, api_key, stock_symbols)
print(json_response)