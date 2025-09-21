"""
Данная программа является учебной.

Задача - выгрузка с Google Drive таблицы данных в формате xlsx
в переменную raw_data.

Для работы с файлами типа csv используется команда pd.read_csv()

"""

import pandas as pd

FILE_ID = "1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U"  # Уникальное ID файла в Google Drive
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

raw_data = pd.read_excel(file_url)  # чтение файла

# print(raw_data.info()) # вывод информации о выгруженной таблице
# with pd.option_context('display.max_columns', None) #функция для отображения всех стобцов в таблице
print(raw_data.head(10))  # вывод первых 10 строк в таблице.
