import os
import pandas as pd


def create_save_dataset(headers, data):
    """
    Загружает данные в Dataframe, преобразует типы и сохраняет в файлы:
    .csv - до типизации
    .parquet - после типизации
    """

    dataset = pd.DataFrame(data, columns=headers)

    os.makedirs("data", exist_ok=True)

    csv_path = "data/world_population.csv"
    dataset.to_csv(csv_path, index=False, encoding="utf-8")

    dataset["Year (July 1)"] = dataset["Year (July 1)"].astype(int)
    dataset["Population"] = dataset["Population"].astype("int64")
    dataset["Yearly % Change"] = dataset["Yearly % Change"].astype(float) / 100
    dataset["Yearly Change"] = dataset["Yearly Change"].astype(float).astype("int64")
    dataset["Median Age"] = dataset["Median Age"].astype(float) / 10000
    dataset["Fertility Rate"] = dataset["Fertility Rate"].astype(float) / 10000
    dataset["Density (P/Km²)"] = dataset["Density (P/Km²)"].astype(float)

    parquet_path = "data/world_population.parquet"
    dataset.to_parquet(parquet_path, index=False)

    return dataset
