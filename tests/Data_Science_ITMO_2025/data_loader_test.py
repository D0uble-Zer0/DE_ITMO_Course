import os
import requests
import pandas as pd


def check_xlsx_exists():
    """Проверяет наличие xlsx файла в папке data"""
    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    if not os.path.exists(data_path):
        os.makedirs(data_path)
        return False

    for f in os.listdir(data_path):
        if f.endswith(".xlsx"):
            return os.path.join(data_path, f)

    return False


def download_dataset(FILE_ID):
    """Скачивает dataset с Google Drive"""
    src_path = os.path.dirname(__file__)
    project_path = os.path.dirname(src_path)
    data_path = os.path.join(project_path, "data")

    file_url = f"https://drive.google.com/uc?id={FILE_ID}"
    response = requests.get(file_url)

    file_path = os.path.join(data_path, "dataset.xlsx")
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Dataset скачан в: {file_path}")
    return file_path


def load_data():
    """Основная функция загрузки данных"""
    FILE_ID = "-----"  # Уникальное ID файла в Google Drive

    # Проверяем наличие файла
    file_path = check_xlsx_exists()

    if not file_path:
        print("XLSX файл не найден, скачиваем...")
        file_path = download_dataset(FILE_ID)
    else:
        print(f"Найден файл: {file_path}")

    raw_data = pd.read_excel(file_path)
    return raw_data
