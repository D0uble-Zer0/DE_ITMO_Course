import pandas as pd
import os


def check_parquet_file(filename="dataset.parquet"):
    """
    Проверка в директории data dataset.parquet.
    """

    src_path = os.path.dirname(__file__)
    d_path = os.path.join(src_path, "data")  # добавляем путь к data

    f_path = os.path.join(d_path, filename)
    return f_path if os.path.exists(f_path) else False


def save_parquet(data, filename="dataset.parquet"):
    """
    Сохраняем dataset из .xlsx в .parquet
    """

    src_path = os.path.dirname(__file__)
    d_path = os.path.join(src_path, "data")

    f_path = os.path.join(d_path, filename)

    data.to_parquet(f_path, index=False)  # сохраняем dataset в .parquet

    return f_path


def load_parquet(filename="dataset.parquet"):
    """
    Загружаем данные из .parquet в main.
    """
    f_path = check_parquet_file(filename)
    if f_path:
        return pd.read_parquet(f_path)
    else:
        raise FileNotFoundError(f"\Parquet файл не найден")
