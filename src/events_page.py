import pandas as pd
from datetime import datetime, timedelta
import json
from home_page import load_excel_to_dataframe, get_currency_rates, get_stock_prices


def total_income(df: pd.DataFrame) -> int:
    """__"""
    return int(df[df['Сумма платежа'] > 0]['Сумма платежа'].sum())



def total_expenses(df: pd.DataFrame) -> int:
    """Возвращает общую сумму расходов из датафрейма"""
    return int(df['Сумма платежа'].sum())

def get_main_expenses(df: pd.DataFrame, n: int) -> list:
    """Возвращает основные расходы по категориям"""
    main_expenses = df.groupby('Категория')['Сумма платежа'].sum().reset_index()
    main_expenses = main_expenses.sort_values(by='Сумма платежа', ascending=False).head(n)
    other_expenses = main_expenses.iloc[n:]['Сумма платежа'].sum()
    other_expense_row = pd.DataFrame({'Категория': ['Остальное'], 'Сумма платежа': [other_expenses]})
    main_expenses = pd.concat([main_expenses.head(n - 1), other_expense_row], ignore_index=True)
    main_expenses = [{'category': row['Категория'], 'amount': int(row['Сумма платежа'])} for _, row in main_expenses.iterrows()]
    return main_expenses





def get_transfers_and_cash(df: pd.DataFrame) -> list:
    """Возвращает сумму по категориям 'Наличные' и 'Переводы'"""
    transfers_cash = df[df['Категория'].isin(['Наличные', 'Переводы'])]
    transfers_cash = transfers_cash.groupby('Категория')['Сумма платежа'].sum().reset_index()
    transfers_cash = [{'category': row['Категория'], 'amount': int(row['Сумма платежа'])} for _, row in
                      transfers_cash.iterrows()]
    return transfers_cash


def get_main_income(df: pd.DataFrame, n: int) -> list:
    """Возвращает основные поступления по категориям"""
    main_income = df.groupby('Категория')['Сумма платежа'].sum().reset_index()
    main_income = main_income.sort_values(by='Сумма платежа', ascending=False).head(n)
    main_income = [{'category': row['Категория'], 'amount': int(row['Сумма платежа'])} for _, row in
                   main_income.iterrows()]
    return main_income





if __name__ == '__main__':
    df = load_excel_to_dataframe('operations.xls')


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


    # Пример использования
    api_key = 'LLFCICMLGVZP3MIE'
    date = '2024-06-15'
    range_type = 'M'
    event_summary = get_event_summary(date, range_type)
    print(json.dumps(event_summary, indent=2, ensure_ascii=False))
