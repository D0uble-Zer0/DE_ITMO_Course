import pandas as pd
import os


def check_parquet_file(filename="dataset.parquet"):
    """

    Функция выполняет проверку нахождения в директории Data файла с названием dataset.parquet.

    """

    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    prj_path = os.path.dirname(src_path)  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(
        prj_path
    )  # поднимаемся на уровень выше (главная директория)
    d_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    f_path = os.path.join(
        d_path, filename
    )  # проверяет есть ли по пути data_path нужный файл filename
    return f_path if os.path.exists(f_path) else False


def save_parquet(data, filename="dataset.parquet"):
    """

    Функция выполняет сохранение данных в формате Parquet в папку data.

    """

    src_path = os.path.dirname(__file__)
    prj_path = os.path.dirname(src_path)
    finall_path = os.path.dirname(prj_path)
    d_path = os.path.join(finall_path, "data")

    f_path = os.path.join(d_path, filename)

    data.to_parquet(f_path, index=False)  # сохраняем dataset в расширении parquet
    print(f"\nДанные сохранены в: {f_path}")
    return f_path


def load_parquet(filename="dataset.parquet"):
    """

    Функция загружает данные из файла parquet в код.

    """
    f_path = check_parquet_file(filename)
    if f_path:
        return pd.read_parquet(f_path)
    else:
        raise FileNotFoundError(f"\Parquet файл {filename} не найден")
