import os
import requests
import pandas as pd


def check_xlsx_exists():
    """

    Функция проверяет нахождение файла xslx в директории data.

    """
    src_path = os.path.dirname(__file__)  # директория где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(
        project_path
    )  # поднимаемся на уровень выше (главная директория)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print("Директория Data отсутствует. Создаем в корне...")
        return False

    for f in os.listdir(data_path):
        if f.endswith(".xlsx"):
            return os.path.join(data_path, f)

    return False


def download_dataset(FILE_ID):
    """

    Функция выполняет скачивание dataset c Google Drive.

    """
    src_path = os.path.dirname(__file__)
    project_path = os.path.dirname(src_path)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")

    file_url = (
        f"https://drive.google.com/uc?id={FILE_ID}"  # заходим в Google Drive в dataset
    )
    response = requests.get(file_url)
    file_path = os.path.join(data_path, "dataset.xlsx")
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"\nDataset загружен в: {file_path}")
    return file_path


def load_data():
    """

    Функция выполняет загрузку данных.

    """
    FILE_ID = "1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U"  # уникальное ID файла в Google Drive

    file_path = check_xlsx_exists()  # проверяем наличие файла

    if not file_path:
        file_path = download_dataset(FILE_ID)
    else:
        print(f"Найден файл: {file_path}")

    raw_data = pd.read_excel(file_path)
    data_with_NaN = raw_data.replace("-", pd.NA)
    return data_with_NaN
