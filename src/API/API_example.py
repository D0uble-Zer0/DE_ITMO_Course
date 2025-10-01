"""
Программа запрашивает с API данные об пивоварнях в США.
Является примером реализации выгрузки dataset с открытых API.
"""

from get_user_API import get_user_input
from data_from_API import download_data
from data_saver_API import convert_to_dataset_and_save


num_download_breweries = get_user_input()  # вписываем количество искомых пивоварен.

print(f"\n{'-'*60}")
print("Этап 1: Загрузка данных из API")
print(f"{'-'*60}")
breweries = download_data(num_download_breweries)

if not breweries:
    print("ERROR - не удалось загрузить данные")

print(f"\n{'-'*60}")
print("Этап 2: Сохранения данных")
print(f"{'-'*60}")
result = convert_to_dataset_and_save(breweries)

if result is not None:
    print(f"\n{'-' * 60}")
    print("Этап 3: Анализ датасета")
    print(f"{'-' * 60}")
    print(result.info())
