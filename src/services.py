import pandas as pd
from pandas import DataFrame


def load_excel_to_dataframe(file_name: str) -> DataFrame:
    """Функция читает эксель файл и возвращает дата фрейм"""
    # Чтение данных из Excel файла
    df = pd.read_excel(file_name)
    return df


if __name__ == '__main__':
    file_name = 'operations.xls'
    dataframe = load_excel_to_dataframe(file_name)
    print(dataframe)
