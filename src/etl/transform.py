import pandas as pd


def data_after_transform(raw_data):
    """
    Очищаем dataset от ошибок и производим типизацию данных.
    """

    conv_data = raw_data.copy()
    conv_data = conv_data.replace("-", pd.NA)
    conv_data = conv_data.drop(
        ["Cylinders", "Drive wheels", "Color", "Airbags"], axis=1
    )

    conv_data["Levy"] = conv_data["Levy"].astype(
        "Int16"
    )  # данный тип данных позволяет преобразовать признак с пропусками
    conv_data["Levy"] = conv_data["Levy"].fillna(conv_data["Levy"].median())

    conv_data["Mileage"] = conv_data["Mileage"].str.replace(" km", "", regex=False)
    conv_data["Mileage"] = conv_data["Mileage"].astype("int32")

    conv_data = conv_data.drop_duplicates()

    conv_data = conv_data.rename(
        columns={
            "Levy": "Tax",
            "Prod. year": "Release_year",
            "Category": "Car_type",
            "Gear box type": "Transmission_type",
        }
    )

    conv_data["Price"] = conv_data["Price"].mask(
        conv_data["Price"] > 900000, conv_data["Price"].median()
    )

    Q1_Mil = conv_data["Mileage"].quantile(0.25)
    Q3_Mil = conv_data["Mileage"].quantile(0.75)
    IQR_Mil = Q3_Mil - Q1_Mil
    up_bound_Mil = Q3_Mil + 1.5 * IQR_Mil

    conv_data = conv_data[conv_data["Mileage"] <= up_bound_Mil]

    conv_data["ID"] = conv_data["ID"].astype("int32")
    conv_data["Price"] = conv_data["Price"].astype("int32")
    conv_data["Manufacturer"] = conv_data["Manufacturer"].astype("category")
    conv_data["Model"] = conv_data["Model"].astype("category")
    conv_data["Tax"] = conv_data["Tax"].astype("int32")
    conv_data["Release_year"] = conv_data["Release_year"].astype("int16")
    conv_data["Car_type"] = conv_data["Car_type"].astype("category")
    conv_data["Have a leather interior?"] = (
        conv_data["Leather interior"].map({"No": 0, "Yes": 1}).astype("bool")
    )  # добавляем к оригинальному признаку  булевый признак.

    conv_data["Car have a left wheel?"] = (
        conv_data["Wheel"].map({"Right-hand drive": 0, "Left wheel": 1}).astype("bool")
    )

    conv_data["Fuel type"] = conv_data["Fuel type"].astype("category")
    conv_data["Transmission_type"] = conv_data["Transmission_type"].astype("category")
    conv_data["Doors"] = conv_data["Doors"].astype("category")
    conv_data[["Leather interior", "Wheel"]] = conv_data[
        ["Have a leather interior?", "Car have a left wheel?"]
    ]  # заменяем оригинал на булевый.
    conv_data = conv_data.drop(
        columns=["Have a leather interior?", "Car have a left wheel?"]
    )  # удаляем дополнительные признаки.

    conv_data.rename(
        columns={"Leather interior": "Have a leather interior?"}, inplace=True
    )  # переименовываем.
    conv_data.rename(columns={"Wheel": "Car have a left wheel?"}, inplace=True)

    new_column_names = {
        col: col.lower() for col in conv_data.columns
    }  # снижаем регистр всех букв в нижний
    new_column_names["Have a leather interior?"] = "have_a_leather_interior"
    new_column_names["Fuel type"] = "fuel_type"
    new_column_names["Engine volume"] = "engine_volume"
    new_column_names["Car have a left wheel?"] = "car_have_a_left_wheel"

    clean_data = conv_data.rename(columns=new_column_names)

    return clean_data
