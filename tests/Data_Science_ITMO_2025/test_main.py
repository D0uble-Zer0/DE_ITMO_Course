import pandas as pd
from data_loader_test import load_data, check_xlsx_exists
from data_preprocessor_test import preprocess_data
from data_saver_test import save_to_parquet, check_parquet_exists, load_from_parquet


def main():
    # Проверяем наличие обработанного Parquet файла
    parquet_file = check_parquet_exists()

    if parquet_file:
        print(f"Найден обработанный файл: {parquet_file}")
        print("Загружаем данные из Parquet...")
        processed_data = load_from_parquet()

        print("\nДанные из Parquet файла:")
        print(processed_data.head(10))
        print("\nИнформация о типах данных:")
        print(processed_data.info())

    else:
        print("Обработанный Parquet файл не найден, начинаем обработку...")

        # Проверяем наличие исходного XLSX файла
        if not check_xlsx_exists():
            print("Исходный XLSX файл не найден, будет выполнена загрузка...")

        # Загрузка данных
        raw_data = load_data()
        data_with_NaN = raw_data.replace("-", pd.NA)

        print("\nДанные до обработки:")
        print(data_with_NaN.head(10))
        print("\nИнформация о типах данных до обработки:")
        print(data_with_NaN.info())

        # Предобработка данных
        processed_data = preprocess_data(data_with_NaN)

        # Сохранение в Parquet
        file_path = save_to_parquet(processed_data)

        print("\nДанные после обработки:")
        print(processed_data.head(10))
        print("\nИнформация о типах данных после обработки:")
        print(processed_data.info())
        print(f"\nФайл сохранен: {file_path}")


if __name__ == "__main__":
    main()
