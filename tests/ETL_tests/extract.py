import os
import requests
import pandas as pd


def load_dataset_from_GD(data_dir, file_id):
    """
    Скачиваем dataset c Google Drive.
    """
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    f_path = os.path.join(data_dir, "dataset.xlsx")
    with open(f_path, "wb") as f:
        f.write(response.content)
    return f_path


def load_data_from_xlsx(f_path):
    """
    Загружаем данные из xlsx файла
    """
    dirty_data = pd.read_excel(f_path)
    return dirty_data


def read_data_from_parquet(file_path):
    """
    Загружаем данные из .parquet
    """
    f_path = os.path.join(file_path)

    if os.path.exists(f_path):
        return pd.read_parquet(f_path)
    else:
        raise FileNotFoundError("Ошибка чтения файла .parquet")
