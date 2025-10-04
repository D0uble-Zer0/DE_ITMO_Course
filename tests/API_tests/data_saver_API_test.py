import pandas as pd
import os

OUTPUT_FILENAME = "data/breweries.csv"  # имя файла для пивоварен


def convert_to_dataset_and_save(data: list[dict]) -> pd.DataFrame | None:
    """
    Сохраняет данные в CSV файл
    """
    if not data:
        print("ERROR! Нет данных для сохранения!")
        return None

    os.makedirs("data", exist_ok=True)

    dataset = pd.DataFrame(data)

    dataset["brewery_type"] = dataset["brewery_type"].astype("category")
    dataset["city"] = dataset["city"].astype("category")
    dataset["state_province"] = dataset["state_province"].astype("category")
    dataset["country"] = dataset["country"].astype("category")
    dataset["state"] = dataset["state"].astype("category")

    dataset.to_csv(OUTPUT_FILENAME, index=False)

    print(f"\nДанные сохранены")

    return dataset
