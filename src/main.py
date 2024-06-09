#ГЛАВНАЯ СТРАНИЦА
import json

from src.home_page import load_excel_to_dataframe, get_greeting, get_card_summary, get_top_transactions, \
    get_currency_rates, get_stock_prices

file_name = 'operations.xls'
api_key = 'LLFCICMLGVZP3MIE'
stock_symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']


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






#СТРАНИЦА СОБЫТИЙ

def get_event_summary(date: str, range_type: str = 'M') -> dict:
    """Возвращает JSON-ответ с данными о расходах и поступлениях"""
    # Фильтрация данных по дате
    start_date = None
    if range_type == 'W':
        start_date = datetime.strptime(date, '%Y-%m-%d') - timedelta(
            days=datetime.strptime(date, '%Y-%m-%d').weekday())
    elif range_type == 'M':
        start_date = datetime.strptime(date, '%Y-%m-%d').replace(day=1)
    elif range_type == 'Y':
        start_date = datetime.strptime(date, '%Y-%m-%d').replace(month=1, day=1)
    elif range_type == 'ALL':
        start_date = datetime.strptime('2000-01-01', '%Y-%m-%d')  # Дата начала данных
    else:
        raise ValueError('Invalid range_type. Should be one of: W, M, Y, ALL')

    # Преобразование 'Дата операции' в datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    filtered_df = df[df['Дата операции'].between(start_date, datetime.strptime(date, '%Y-%m-%d'))]

    # Формирование JSON-ответа
    event_summary = {
        'expenses': {
            'total_amount': total_expenses(filtered_df),
            'main': get_main_expenses(filtered_df, 7),
            'transfers_and_cash': get_transfers_and_cash(filtered_df)
        },
        'income': {
            'total_amount': total_income(filtered_df),
            'main': get_main_income(filtered_df, 3)
        },
        'currency_rates': get_currency_rates(),
        'stock_prices': get_stock_prices(api_key, ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA'])
    }
    return event_summary



print('ГЛАВНАЯ СТРАНИЦА')
json_response = main(file_name, api_key, stock_symbols)
print(json_response)

print('СТРАНИЦА СОБЫТИЙ')
date = '2024-06-15'
range_type = 'M'
event_summary = get_event_summary(date, range_type
print(json.dumps(event_summary, indent=2, ensure_ascii=False))