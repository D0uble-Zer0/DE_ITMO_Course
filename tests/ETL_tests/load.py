import pandas as pd
import os


def save_data_to_parquet(data, data_dir, filename="dataset.parquet"):
    """
    Сохраняем dataset в .parquet
    """

    f_path = os.path.join(data_dir, filename)
    data.to_parquet(f_path, index=False)
    return f_path
