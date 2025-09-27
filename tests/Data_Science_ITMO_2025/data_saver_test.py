import pandas as pd
import os


def check_parquet_exists(filename="processed_data.parquet"):
    """Проверяет наличие parquet файла в папке data"""
    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    file_path = os.path.join(data_path, filename)
    return file_path if os.path.exists(file_path) else False


def save_to_parquet(data, filename="processed_data.parquet"):
    """
    Функция для сохранения данных в формате Parquet в папку data
    """
    # Определяем пути
    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    # Создаем папку data если ее нет
    os.makedirs(data_path, exist_ok=True)

    # Полный путь к файлу
    file_path = os.path.join(data_path, filename)

    # Сохраняем в Parquet
    data.to_parquet(file_path, index=False)
    print(f"Данные сохранены в: {file_path}")

    return file_path


def load_from_parquet(filename="processed_data.parquet"):
    """Загружает данные из Parquet файла"""
    file_path = check_parquet_exists(filename)
    if file_path:
        return pd.read_parquet(file_path)
    else:
        raise FileNotFoundError(f"Parquet файл {filename} не найден")
