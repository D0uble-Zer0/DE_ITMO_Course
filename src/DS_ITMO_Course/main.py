"""
Программа реализует выгрузку файла с Google Drive, приведение типов данных выгруженного dataset
и его сохранение в .parquet.

Добавлен для проверки вывод info()
"""

from data_loader import load_data, check_xlsx_file
from data_conversion import conversion_of_data
from data_saver import save_parquet, check_parquet_file, load_parquet

print(f"\n{'-'*60}")
print("Этап 0: Проверка наличия dataset в формате parquet")
print(f"{'-'*60}")
parquet_dataset = check_parquet_file()

if parquet_dataset:
    print("Найден файл .parquet")
    data = load_parquet()
    print(f"\n{'-' * 60}")
    print("Этап 3: Вывод информации dataset после приведения типов")
    print(f"{'-' * 60}")
    print("\nИнформация о типах данных:")
    print(data.info())

else:
    print(f"\n{'-' * 60}")
    print("Этап 1: Проверка наличия dataset в формате xlsx и его загрузка")
    print(f"{'-' * 60}")
    print("Parquet файл не найден")

    if not check_xlsx_file():
        print("xlsx файл не найден")

    raw_data = load_data()
    print(f"\n{'-' * 60}")
    print("Этап 2: Вывод информации dataset до приведения типов")
    print(f"{'-' * 60}")

    print(raw_data.info())

    data = conversion_of_data(raw_data)

    f_path = save_parquet(data)
    print(f"\n{'-' * 60}")
    print("Этап 3: Вывод информации dataset после приведения типов")
    print(f"{'-' * 60}")

    print(data.info())
