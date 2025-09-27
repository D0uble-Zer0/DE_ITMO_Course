import pandas as pd


def preprocess_data(data_with_NaN):
    """
    Функция для предобработки данных: замены ошибочных значений и приведения типов
    """
    # Создаем копию, чтобы не изменять исходные данные
    processed_data = data_with_NaN.copy()

    # Блок замены ошибочных значений
    processed_data.loc[processed_data["Price"] == 26307500, "Price"] = 5980

    # Обработка Mileage
    processed_data["Mileage"] = processed_data["Mileage"].str.replace(
        " km", "", regex=False
    )
    processed_data["Mileage"] = pd.to_numeric(
        processed_data["Mileage"], errors="coerce"
    )
    processed_data["Mileage"] = processed_data["Mileage"].where(
        processed_data["Mileage"] <= 7600000
    )
    mean_mileage = processed_data["Mileage"].mean()
    processed_data["Mileage"] = processed_data["Mileage"].fillna(mean_mileage)

    # Приведение типов
    processed_data["ID"] = processed_data["ID"].astype("int32")
    processed_data["Price"] = processed_data["Price"].astype("int32")
    processed_data["Levy"] = pd.to_numeric(
        processed_data["Levy"], errors="coerce"
    ).astype("Int16")
    processed_data["Manufacturer"] = processed_data["Manufacturer"].astype("category")
    processed_data["Model"] = processed_data["Model"].astype("category")
    processed_data["Prod. year"] = processed_data["Prod. year"].astype("int8")
    processed_data["Category"] = processed_data["Category"].astype("category")

    # Преобразование булевых колонок
    processed_data["Have a leather interior?"] = (
        processed_data["Leather interior"].map({"No": 0, "Yes": 1}).astype("bool")
    )
    processed_data["Car have a left wheel?"] = (
        processed_data["Wheel"]
        .map({"Right-hand drive": 0, "Left wheel": 1})
        .astype("bool")
    )

    processed_data["Fuel type"] = processed_data["Fuel type"].astype("category")
    processed_data["Mileage"] = processed_data["Mileage"].astype("int32")
    processed_data["Cylinders"] = processed_data["Cylinders"].astype("int8")
    processed_data["Gear box type"] = processed_data["Gear box type"].astype("category")
    processed_data["Drive wheels"] = processed_data["Drive wheels"].astype("category")
    processed_data["Doors"] = processed_data["Doors"].astype("category")
    processed_data["Color"] = processed_data["Color"].astype("category")
    processed_data["Airbags"] = processed_data["Airbags"].astype("int8")

    processed_data[["Leather interior", "Wheel"]] = processed_data[
        ["Have a leather interior?", "Car have a left wheel?"]
    ]
    processed_data = processed_data.drop(
        columns=["Have a leather interior?", "Car have a left wheel?"]
    )

    processed_data.rename(
        columns={"Leather interior": "Have a leather interior?"}, inplace=True
    )
    processed_data.rename(columns={"Wheel": "Car have a left wheel?"}, inplace=True)

    return processed_data
