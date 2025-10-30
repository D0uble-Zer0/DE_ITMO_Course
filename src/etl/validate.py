import os
import pandas as pd


def check_file_parquet(processed_dir, filename):
    """
    Проверка в директории .parquet
    """
    file_path = os.path.join(processed_dir, filename)
    return os.path.exists(file_path)


def check_file_xlsx(raw_dir, filename):
    """
    Проверка в директории .xlsx
    """
    file_path = os.path.join(raw_dir, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        return False


def validate_xlsx_data(dirty_data):
    """
    Валидация исходных данных
    """
    print(f"\n{'=' * 60}")
    print("--ПРОВЕРКА ВХОДНЫХ ДАННЫХ--")
    print(f"{'=' * 60}\n")

    print("\n Пункт 1 -> Пропуски:\n")
    dirty_data = dirty_data.replace("-", pd.NA)
    empty_val = dirty_data.isnull().sum()
    for col, count in empty_val.items():
        if count >= 0:
            print(f"   - {col}: {count} пропусков")

    print("\n Пункт 2 -> Cтолбцы:\n")
    columns = [
        "ID",
        "Price",
        "Levy",
        "Manufacturer",
        "Model",
        "Prod. year",
        "Category",
        "Leather interior",
        "Fuel type",
        "Engine volume",
        "Mileage",
        "Cylinders",
        "Gear box type",
        "Drive wheels",
        "Doors",
        "Wheel",
        "Color",
        "Airbags",
    ]
    for col in columns:
        if col in dirty_data.columns:
            print(f"   - {col}: Присутствуют")
        else:
            print(f"   - {col}: Отсутствуют")

    print(f"\n Пункт 3 -> Дубликаты: {dirty_data.duplicated().sum()} записей\n")

    print(f"\n{'=' * 60}")
    print("--ЗАВЕРШЕНО--")
    print(f"{'=' * 60}\n")


def validate_parquet_data(data):
    """
    Валидация выходных данных
    """
    print(f"\n{'=' * 60}")
    print("--ПРОВЕРКА ВЫХОДНЫХ ДАННЫХ--")
    print(f"{'=' * 60}\n")

    errors = False

    print("\n Пункт 1 -> Пропуски:\n")
    empty_val = data.isnull().sum()
    for col, count in empty_val.items():
        if count >= 0:
            print(f"   - {col}: {count} пропусков")

    print("\n Пункт 2 -> Типы данных:\n")
    features_types = {
        "id": "int32",
        "price": "int32",
        "tax": "int32",
        "manufacturer": "category",
        "model": "category",
        "release_year": "int16",
        "car_type": "category",
        "fuel_type": "category",
        "engine_volume": "object",
        "mileage": "int32",
        "transmission_type": "category",
        "doors": "category",
        "have_a_leather_interior": "bool",
        "car_have_a_left_wheel": "bool",
    }.items()

    for col, expected_type in features_types:
        if col in data.columns:
            actual_type = str(data[col].dtype)
            status = (
                "Успешно"
                if actual_type == expected_type
                else f"Провалено (ожидался {expected_type})"
            )
            print(f"   - {col}: {actual_type} {status}")

            if actual_type != expected_type:
                errors = True
        else:
            print(f"   - {col}: ОТСУТСТВУЕТ")
            errors = True

    print(f"\n Пункт 3 -> Дубликаты: {data.duplicated().sum()} записей\n")

    if data.duplicated().sum() > 0:
        errors = True

    print(f"\n{'=' * 60}")
    print("--ЗАВЕРШЕНО--")
    print(f"{'=' * 60}")

    return not errors  # True если ошибок нет, False если есть ошибки
