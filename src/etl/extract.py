import os
import requests
import pandas as pd


def load_dataset_from_GD(raw_dir, file_id, filename):
    """
    Скачиваем dataset c Google Drive.
    """
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    f_path = os.path.join(raw_dir, filename)
    with open(f_path, "wb") as f:
        f.write(response.content)
    return f_path


def load_data_from_xlsx(f_path):
    """
    Загружаем данные из xlsx файла
    """
    dirty_data = pd.read_excel(f_path)
    return dirty_data
