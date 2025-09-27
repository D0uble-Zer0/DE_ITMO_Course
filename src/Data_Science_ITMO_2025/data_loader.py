import os
import requests
import pandas as pd


def check_xlsx_file():
    """

    Функция проверяет нахождение файла xlsx в директории data.

    """
    src_path = os.path.dirname(__file__)  # директория где лежит этот скрипт (src)
    prj_path = os.path.dirname(src_path)  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(
        prj_path
    )  # поднимаемся на уровень выше (главная директория)
    d_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    if not os.path.exists(d_path):
        os.makedirs(d_path)
        print("Директория Data отсутствует. Создаем в корне...")
        return False

    for f in os.listdir(d_path):
        if f.endswith(".xlsx"):
            return os.path.join(d_path, f)

    return False


def download_dataset(FILE_ID):
    """

    Функция выполняет скачивание dataset c Google Drive.

    """
    src_path = os.path.dirname(__file__)
    prj_path = os.path.dirname(src_path)
    finall_path = os.path.dirname(prj_path)
    d_path = os.path.join(finall_path, "data")

    file_url = (
        f"https://drive.google.com/uc?id={FILE_ID}"  # заходим в Google Drive в dataset
    )
    response = requests.get(file_url)
    file_path = os.path.join(d_path, "dataset.xlsx")
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"\nDataset загружен в: {file_path}")
    return file_path


def load_data():
    """

    Функция выполняет загрузку данных.

    """
    FILE_ID = "1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U"  # уникальное ID файла в Google Drive

    f_path = check_xlsx_file()  # проверяем наличие файла

    if not f_path:
        f_path = download_dataset(FILE_ID)
    else:
        print(f"Найден файл: {f_path}")

    raw_data = pd.read_excel(f_path)
    data_with_NaN = raw_data.replace("-", pd.NA)
    return data_with_NaN
