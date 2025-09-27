from data_loader import load_data, check_xlsx_file
from data_conversion import conversion_of_data
from data_saver import save_parquet, check_parquet_file, load_parquet


parquet_dataset = (
    check_parquet_file()
)  # проверяет наличие в директории data файла .parquet

if parquet_dataset:
    print(f"Найден файл: {parquet_dataset}")
    data = load_parquet()
    print("\nИнформация о типах данных:")
    print(data.info())

else:
    print("Parquet файл не найден...")

    if not check_xlsx_file():  # проверяем наличие в директории data файла .xlsx
        print("xlsx файл не найден...")

    raw_data = load_data()  # загружаем данные
    print("\nИнформация о типах данных до приведения типов:")
    print(raw_data.info())

    data = conversion_of_data(raw_data)  # приведение типов данных

    f_path = save_parquet(data)  # сохранение в формате .parquet

    print("\nИнформация о типах данных после приведение типов:")
    print(data.info())
