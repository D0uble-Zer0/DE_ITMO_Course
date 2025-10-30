import pandas as pd


def conversion_of_data(raw_data):
    """
    Очищаем dataset от ошибок и производим типизацию данных.
    """

    # ------------Блок очистки ошибок------------
    conv_data = raw_data.copy()
    conv_data.loc[conv_data["Price"] == 26307500, "Price"] = 5980  # замена выброса
    conv_data["Mileage"] = conv_data["Mileage"].str.replace(
        " km", "", regex=False
    )  # отделяем от чисел текст "km"

    conv_data["Mileage"] = pd.to_numeric(
        conv_data["Mileage"], errors="coerce"
    )  # переводим для обработки. Иначе не дает работать.

    conv_data["Mileage"] = conv_data["Mileage"].where(conv_data["Mileage"] <= 7600000)
    mean_mileage = conv_data["Mileage"].mean()
    conv_data["Mileage"] = conv_data["Mileage"].fillna(
        mean_mileage
    )  # заполнение всех NaN средним значением.

    # ------------Блок приведения типов------------
    conv_data["ID"] = conv_data["ID"].astype("int32")

    conv_data["Price"] = conv_data["Price"].astype("int32")

    conv_data["Levy"] = pd.to_numeric(conv_data["Levy"], errors="coerce").astype(
        "Int16"
    )  # необходимость усложнения, так как тип Int, в отличии от int, может пропускать NaN.

    conv_data["Manufacturer"] = conv_data["Manufacturer"].astype("category")

    conv_data["Model"] = conv_data["Model"].astype("category")

    conv_data["Prod. year"] = conv_data["Prod. year"].astype("int8")

    conv_data["Category"] = conv_data["Category"].astype("category")

    conv_data["Have a leather interior?"] = (
        conv_data["Leather interior"].map({"No": 0, "Yes": 1}).astype("bool")
    )  # добавляем к оригинальному признаку  булевый признак.

    conv_data["Car have a left wheel?"] = (
        conv_data["Wheel"].map({"Right-hand drive": 0, "Left wheel": 1}).astype("bool")
    )

    conv_data["Fuel type"] = conv_data["Fuel type"].astype("category")

    conv_data["Mileage"] = conv_data["Mileage"].astype("int32")

    conv_data["Cylinders"] = conv_data["Cylinders"].astype("int8")

    conv_data["Gear box type"] = conv_data["Gear box type"].astype("category")

    conv_data["Drive wheels"] = conv_data["Drive wheels"].astype("category")

    conv_data["Doors"] = conv_data["Doors"].astype("category")

    conv_data["Color"] = conv_data["Color"].astype("category")

    conv_data["Airbags"] = conv_data["Airbags"].astype("int8")

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

    return conv_data
