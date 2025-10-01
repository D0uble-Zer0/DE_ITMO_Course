import os
import requests
import pandas as pd


def check_xlsx_file():
    """
    Проверка в директории data dataset.xlsx
    """
    src_path = os.path.dirname(__file__)
    d_path = os.path.join(src_path, "data")

    if not os.path.exists(d_path):
        os.makedirs(d_path)
        print("Директория Data отсутствует. Создаем...")
        return False

    for f in os.listdir(d_path):
        if f.endswith(".xlsx"):
            return os.path.join(d_path, f)  # возвращаем путь к файлу

    return False


def download_dataset(FILE_ID):
    """
    Скачиваем dataset c Google Drive.
    """
    src_path = os.path.dirname(__file__)
    d_path = os.path.join(src_path, "data")

    file_url = f"https://drive.google.com/uc?id={FILE_ID}"  # заходим в Google Drive
    response = requests.get(file_url)
    f_path = os.path.join(d_path, "dataset.xlsx")
    with open(f_path, "wb") as f:
        f.write(response.content)
    return f_path


def load_data():
    """
    Загружаем данные в main
    """
    FILE_ID = "1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U"  # уникальное ID файла в Google Drive

    f_path = check_xlsx_file()

    if not f_path:
        f_path = download_dataset(FILE_ID)

    raw_data = pd.read_excel(f_path)
    data_NaN = raw_data.replace("-", pd.NA)  # убираем все ложные пропуски на NaN
    return data_NaN
