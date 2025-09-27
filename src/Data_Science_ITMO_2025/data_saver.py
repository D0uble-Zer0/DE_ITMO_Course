import pandas as pd
import os


def check_parquet_exists(filename="dataset.parquet"):
    """

    Функция выполняет проверку нахождения в директории Data файла с названием dataset.parquet.

    """

    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(
        project_path
    )  # поднимаемся на уровень выше (главная директория)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    file_path = os.path.join(
        data_path, filename
    )  # проверяет есть ли по пути data_path нужный файл filename
    return file_path if os.path.exists(file_path) else False


def save_to_parquet(data, filename="dataset.parquet"):
    """

    Функция выполняет сохранение данных в формате Parquet в папку data.

    """

    src_path = os.path.dirname(__file__)
    project_path = os.path.dirname(src_path)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")

    file_path = os.path.join(data_path, filename)

    data.to_parquet(file_path, index=False)  # сохраняем dataset в расширении parquet
    print(f"\nДанные сохранены в: {file_path}")
    return file_path


def load_from_parquet(filename="dataset.parquet"):
    """

    Функция загружает данные из файла parquet в код.

    """
    file_path = check_parquet_exists(filename)
    if file_path:
        return pd.read_parquet(file_path)
    else:
        raise FileNotFoundError(f"\Parquet файл {filename} не найден")
