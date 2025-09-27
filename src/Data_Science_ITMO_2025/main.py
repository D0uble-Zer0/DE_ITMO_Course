from data_loader import load_data, check_xlsx_exists
from data_conversion import conversion_of_data
from data_saver import save_to_parquet, check_parquet_exists, load_from_parquet


parquet_file = (
    check_parquet_exists()
)  # проверяет наличие в директории data файла .parquet

if parquet_file:
    print(f"Найден файл: {parquet_file}")
    data = load_from_parquet()
    print("\nИнформация о типах данных:")
    print(data.info())

else:
    print("Parquet файл не найден...")

    if not check_xlsx_exists():  # проверяем наличие в директории data файла .xslx
        print("xlsx файл не найден...")

    raw_data = load_data()  # загружаем данные
    print("\nИнформация о типах данных до приведения типов:")
    print(raw_data.info())

    data = conversion_of_data(raw_data)  # приведение типов данных

    file_path = save_to_parquet(data)  # сохранение в формате .parquet

    print("\nИнформация о типах данных после приведение типов:")
    print(data.info())
