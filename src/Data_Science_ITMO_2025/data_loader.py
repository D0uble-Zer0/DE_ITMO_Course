"""
Данная программа является учебной.

Задача - выгрузка с Google Drive таблицы данных в формате xlsx
в создаваемую или уже созданную директорию data.

Для работы с файлами типа csv используется команда pd.read_csv()

"""

import os
import requests
import pandas as pd


def check_and_download_file(
    FILE_ID,
):  # функция проверки файла формата xlsx в директории

    src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
    project_path = os.path.dirname(
        src_path
    )  # поднимаемся на уровень выше (корень проекта)
    finall_path = os.path.dirname(project_path)
    data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

    if not os.path.exists(data_path):
        os.makedirs(data_path)  # проверка наличия папки data в корне проекта
        print("ОШИБКА! Отсутствует папка data!")

    xlsx_files = []

    for f in os.listdir(data_path):
        if f.endswith(".xlsx"):  # Если файл кончается на xlsx
            xlsx_files.append(f)

    if xlsx_files:  # если найден файл xlsx
        file_path = os.path.join(data_path, xlsx_files[0])
        print(f"Найден файл: {xlsx_files[0]}")
        return file_path
    else:  # если файлов нет, загружаем с Google Drive
        file_url = f"https://drive.google.com/uc?id={FILE_ID}"
        response = requests.get(file_url)  # скачиваем файл

        # Сохраняем файл
        file_path = os.path.join(data_path, "dataset.xlsx")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Dataset не найден, скачиваем в: {file_path}")
        return file_path


def load_data():  # основная функция вызова
    FILE_ID = "1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U"  # Уникальное ID файла в Google Drive
    file_path = check_and_download_file(FILE_ID)
    raw_data = pd.read_excel(file_path)  # чтение файла

    return raw_data
