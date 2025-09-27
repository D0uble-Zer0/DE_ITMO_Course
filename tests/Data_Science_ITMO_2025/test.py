import pandas as pd
import os

src_path = os.path.dirname(__file__)  # папка где лежит этот скрипт (src)
project_path = os.path.dirname(src_path)  # поднимаемся на уровень выше (корень проекта)
finall_path = os.path.dirname(project_path)
data_path = os.path.join(finall_path, "data")  # создаем путь к папке data в корне

file_path = os.path.join(data_path, "dataset.xlsx")
raw_data = pd.read_excel(file_path)  # первая загрузка dataset (грязный)
data_with_NaN = raw_data.replace(
    "-", pd.NA
)  # замена ненастоящего пропуска с символом "-" на настоящий NaN.

"""

* Блок замены ошибочных значений *

"""

data_with_NaN.loc[data_with_NaN["Price"] == 26307500, "Price"] = 5980  # заменяем
data_with_NaN["Mileage"] = data_with_NaN["Mileage"].str.replace(
    " km", "", regex=False
)  # убираем построчно значение от приписки km
data_with_NaN["Mileage"] = pd.to_numeric(
    data_with_NaN["Mileage"], errors="coerce"
)  # переводим значения в числа для замены
data_with_NaN["Mileage"] = data_with_NaN["Mileage"].where(
    data_with_NaN["Mileage"] <= 7600000
)  # заменяем значения выше порога на NaN
mean_mileage = data_with_NaN[
    "Mileage"
].mean()  # находим среднее значение столбца (игнорируя NaN)
data_with_NaN["Mileage"] = data_with_NaN["Mileage"].fillna(
    mean_mileage
)  # заполняем пропуски средним значением


"""

Приведение типов

"""

data_with_NaN["ID"] = data_with_NaN["ID"].astype("int32")
data_with_NaN["Price"] = data_with_NaN["Price"].astype("int32")
data_with_NaN["Levy"] = pd.to_numeric(data_with_NaN["Levy"], errors="coerce").astype(
    "Int16"
)
data_with_NaN["Manufacturer"] = data_with_NaN["Manufacturer"].astype("category")
data_with_NaN["Model"] = data_with_NaN["Model"].astype("category")
data_with_NaN["Prod. year"] = data_with_NaN["Prod. year"].astype("int8")
data_with_NaN["Category"] = data_with_NaN["Category"].astype("category")
data_with_NaN["Have a leather interior?"] = (
    data_with_NaN["Leather interior"].map({"No": 0, "Yes": 1}).astype("bool")
)
data_with_NaN["Fuel type"] = data_with_NaN["Fuel type"].astype("category")
data_with_NaN["Mileage"] = data_with_NaN["Mileage"].astype("int32")
data_with_NaN["Cylinders"] = data_with_NaN["Cylinders"].astype("int8")
data_with_NaN["Gear box type"] = data_with_NaN["Gear box type"].astype("category")
data_with_NaN["Drive wheels"] = data_with_NaN["Drive wheels"].astype("category")
data_with_NaN["Doors"] = data_with_NaN["Doors"].astype("category")
data_with_NaN["Car have a left wheel?"] = (
    data_with_NaN["Wheel"].map({"Right-hand drive": 0, "Left wheel": 1}).astype("bool")
)
data_with_NaN["Color"] = data_with_NaN["Color"].astype("category")
data_with_NaN["Airbags"] = data_with_NaN["Airbags"].astype("int8")


data_with_NaN[["Leather interior", "Wheel"]] = data_with_NaN[
    ["Have a leather interior?", "Car have a left wheel?"]
]
data_with_NaN = data_with_NaN.drop(
    columns=["Have a leather interior?", "Car have a left wheel?"]
)

data_with_NaN.rename(
    columns={"Leather interior": "Have a leather interior?"}, inplace=True
)
data_with_NaN.rename(columns={"Wheel": "Car have a left wheel?"}, inplace=True)
