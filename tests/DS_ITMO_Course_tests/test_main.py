"""
Программа реализует выгрузку файла с Google Drive, приведение типов данных выгруженного dataset
и его сохранение в .parquet.

Добавлен для проверки вывод info()
"""

import sys
import os
from data_loader_test import load_data, check_xlsx_file
from data_preprocessor_test import conversion_of_data
from data_saver_test import save_parquet, check_parquet_file, load_parquet

docs_dir = os.path.join(os.path.dirname(__file__), "docs")
os.makedirs(docs_dir, exist_ok=True)

with open(os.path.join(docs_dir, "results.txt"), "w", encoding="utf-8") as f:

    class TXT_and_terminal:
        def __init__(self, *files):
            self.files = files

        def write(self, obj):
            for f in self.files:
                f.write(obj)
                f.flush()

        def flush(self):
            for f in self.files:
                f.flush()

    stdout = sys.stdout  # stdout для вывода в файл

    try:
        sys.stdout = TXT_and_terminal(stdout, f)

        print(f"\n{'-'*60}")
        print("Этап 0: Проверка наличия dataset в формате parquet")
        print(f"{'-'*60}")
        parquet_dataset = check_parquet_file()

        if parquet_dataset:
            print(f"Найден файл .parquet")
            data = load_parquet()
            print(f"\n{'-' * 60}")
            print("Этап 3: Вывод информации dataset после привидения типов")
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
            print("Этап 2: Вывод информации dataset до привидения типов")
            print(f"{'-' * 60}")

            print(raw_data.info())

            data = conversion_of_data(raw_data)

            f_path = save_parquet(data)
            print(f"\n{'-' * 60}")
            print("Этап 3: Вывод информации dataset после привидения типов")
            print(f"{'-' * 60}")

            print(data.info())

    finally:
        sys.stdout = stdout

print(f"\n{'-' * 60}")
print(f"Результаты сохранены в: {os.path.join(docs_dir, 'results.txt')}")
print(f"{'-' * 60}")
