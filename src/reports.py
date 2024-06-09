from datetime import datetime
import pandas as pd


# Декоратор без параметра, записывает в файл с названием по умолчанию
def report_decorator_default(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        output_file = f"{func.__name__}_report.txt"
        with open(output_file, "w", encoding='utf-8') as file:
            file.write(str(result))
        return result
    return wrapper

# Декоратор с параметром, принимает имя файла в качестве параметра
def report_decorator(file_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w", encoding='utf-8') as file:
                file.write(str(result))
            return result
        return wrapper
    return decorator

def load_excel_to_dataframe(file_name: str) -> pd.DataFrame:
    """Функция читает эксель файл и возвращает датафрейм"""
    df = pd.read_excel(file_name)
    return df

@report_decorator_default
def expenses_by_category(df: pd.DataFrame, category: str, date: datetime = None):
    if date is None:
        date = datetime.now()
    start_date = date - pd.DateOffset(months=3)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')  # Преобразование в datetime
    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= date) & (df['Категория'] == category)]
    return filtered_df['Сумма операции'].sum()

@report_decorator_default
def expenses_by_weekday(df: pd.DataFrame, date: datetime = None):
    if date is None:
        date = datetime.now()
    start_date = date - pd.DateOffset(months=3)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')  # Преобразование в datetime
    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= date)]
    filtered_df['День недели'] = filtered_df['Дата операции'].dt.dayofweek
    return filtered_df.groupby('День недели')['Сумма операции'].mean().to_dict()

@report_decorator_default
def expenses_by_workday_weekend(df: pd.DataFrame, date: datetime = None):
    if date is None:
        date = datetime.now()
    start_date = date - pd.DateOffset(months=3)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%М:%С')  # Преобразование в datetime
    filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= date)]
    filtered_df['Тип дня'] = filtered_df['Дата операции'].dt.dayofweek.apply(lambda x: 'Рабочий' if x < 5 else 'Выходной')
    return filtered_df.groupby('Тип дня')['Сумма операции'].mean().to_dict()

if __name__ == '__main__':
    # Пример использования
    file_name = 'operations.xls'
    df = load_excel_to_dataframe(file_name)

    # Генерируем отчеты с именами файлов по умолчанию
    expenses_by_category(df, 'Супермаркеты')
    expenses_by_weekday(df)
    expenses_by_workday_weekend(df)

    # Генерируем отчеты с заданными именами файлов
    @report_decorator('expenses_by_category_custom.txt')
    def expenses_by_category_custom(df: pd.DataFrame, category: str, date: datetime = None):
        if date is None:
            date = datetime.now()
        start_date = date - pd.DateOffset(months=3)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%М:%С')  # Преобразование в datetime
        filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= date) & (df['Категория'] == category)]
        return filtered_df['Сумма операции'].sum()

    expenses_by_category_custom(df, 'Супермаркеты')



if __name__ == '__main__':
    # Пример использования
    file_name = 'operations.xls'
    df = load_excel_to_dataframe(file_name)

    # Генерируем отчеты
    expenses_by_category(df, 'Супермаркеты')
    expenses_by_weekday(df)
    expenses_by_workday_weekend(df)
