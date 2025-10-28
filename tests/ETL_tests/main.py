from extract import load_dataset_from_GD, load_data_from_xlsx, read_data_from_parquet
from transform import data_after_transform
from load import save_data_to_parquet
from validate import check_file_parquet, check_file_xlsx
from dotenv import load_dotenv
import os
import click

load_dotenv()

data_dir = os.getenv("ETL_DATA_DIR")
file_id = os.getenv("FILE_ID")
db_user = os.getenv("ETL_DB_USER")
db_password = os.getenv("ETL_DB_PASSWORD")
db_url = os.getenv("ETL_DB_URL")
db_port = os.getenv("ETL_DB_PORT")
db_root_base = os.getenv("ETL_DB_ROOT_BASE")


def etl_pipeline():

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print(f"\n{'-'*60}")
    print("|Проверка наличия dataset в формате parquet в директории data|")
    print(f"{'-'*60}\n")

    if check_file_parquet(data_dir):
        print("Dataset в формате .parquet найден!\n")
        parquet_path = os.path.join(data_dir, "dataset.parquet")
        data = read_data_from_parquet(parquet_path)
        print(f"\n{'-'*60}")
        print("|Вывод информации dataset после преобразований|")
        print(f"{'-'*60}\n")
        print(data.info())

    else:
        print("Dataset в формате .parquet не найден!\n")
        print(f"\n{'-' * 60}")
        print("|Проверка наличия dataset в формате xlsx в директории data|")
        print(f"{'-' * 60}\n")
        f_path = check_file_xlsx(data_dir)

        if not f_path:
            print("xlsx файл не найден")
            f_path = load_dataset_from_GD(data_dir, file_id)
            dirty_data = load_data_from_xlsx(f_path)
            clean_data = data_after_transform(dirty_data)
            parquet_path = save_data_to_parquet(clean_data, data_dir)
            data = read_data_from_parquet(parquet_path)
            print(f"\n{'-'*60}")
            print("|Вывод информации dataset после преобразований|")
            print(f"{'-'*60}\n")
            print(data.info())

        else:
            print("xlsx файл найден")
            dirty_data = load_data_from_xlsx(f_path)
            clean_data = data_after_transform(dirty_data)
            parquet_path = save_data_to_parquet(clean_data, data_dir)
            data = read_data_from_parquet(parquet_path)
            print(f"\n{'-'*60}")
            print("|Вывод информации dataset после преобразований|")
            print(f"{'-'*60}\n")
            print(data.info())

    print(data.dtypes)


if __name__ == "__main__":
    etl_pipeline()
