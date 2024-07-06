import pandas as pd
from typing import List, Dict, Any

from src.home_page import load_excel_to_dataframe


def analyze_cashback(data: pd.DataFrame, year: int, month: int) -> dict:
    """Анализирует выгодность категорий повышенного кешбэка."""
    filtered_data = data[(data['Год'] == year) & (data['Месяц'] == month)]
    cashback_data = filtered_data[filtered_data['Кэшбэк'] > 0]
    cashback_by_category = cashback_data.groupby('Категория')['Кэшбэк'].sum().astype(int).to_dict()
    return cashback_by_category

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Рассчитывает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    total_savings = 0.0
    for transaction in transactions:
        transaction_date = transaction['Дата операции']
        transaction_amount = transaction['Сумма операции']
        if transaction_date.startswith(month):
            rounded_amount = int(-(-transaction_amount // limit) * limit)  # Округляем вверх до ближайшего limit
            saved_amount = transaction_amount - rounded_amount
            total_savings += saved_amount
    return total_savings

def search_by_string(data: pd.DataFrame, search_string: str) -> List[Dict[str, Any]]:
    """Поиск транзакций по строке в описании или категории."""
    return data[data.apply(lambda x: search_string.lower() in x['Описание'].lower() or
                                      search_string.lower() in x['Категория'].lower(), axis=1)].to_dict(orient='records')

def search_phone_numbers(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Поиск транзакций с мобильными номерами в описании."""
    return data[data['Описание'].str.contains(r'\+\d{1,2}\s\d{3}\s\d{2,3}-\d{2}-\d{2}', regex=True)].to_dict(orient='records')

def search_person_to_person_transfers(data: pd.DataFrame) -> List[Dict[str, Any]]:
    """Поиск транзакций переводов физическим лицам."""
    return data[data['Категория'] == 'Переводы'].apply(lambda x: x if len(x['Описание'].split()) > 1 and '.' in x['Описание'].split()[1] else None, axis=1).dropna().to_dict(orient='records')

if __name__ == '__main__':


    operations = load_excel_to_dataframe('operations.xls')
    print(analyze_cashback(operations,2022, 3))