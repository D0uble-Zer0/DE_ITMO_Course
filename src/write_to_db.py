from sqlalchemy import create_engine, inspect
import pandas as pd
import os
import psycopg2

from dotenv import load_dotenv

"""
Загрузка данных из файла .env
"""
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_url = os.getenv("DB_URL")
db_port = os.getenv("DB_PORT")
db_root_base = os.getenv("DB_ROOT_BASE")
db_name_table = os.getenv("DB_NAME_TABLE")


def load_data(file_path=r"data/data_car.parquet"):
    """
    Загрузка данных из parquet файла
    """
    data = pd.read_parquet(file_path)
    pd.set_option("display.max_rows", 150)
    return data


def preprocess_data(data):
    """
    Предобработка данных: переименование колонок
    """
    new_column_names = {col: col.lower() for col in data.columns}
    new_column_names["Have a leather interior?"] = "have_a_leather_interior"
    new_column_names["Fuel type"] = "fuel_type"
    new_column_names["Engine volume"] = "engine_volume"
    new_column_names["Car have a left wheel?"] = "car_have_a_left_wheel"

    data.rename(columns=new_column_names, inplace=True)
    data_processed = data.head(100)
    return data_processed


def check_table_and_data(engine, table_name):
    """
    Проверка таблицы и вывод данных
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema="public")
    if table_name in tables:
        print(f"Ваша таблица найдена!!!")
        print(f"Текущие таблицы в схеме 'public': {tables}")

        with engine.begin() as conn:
            df_sample = pd.read_sql(
                f"SELECT * FROM public.{table_name} LIMIT 100", con=conn
            )
            print(
                df_sample.to_string(index=False)
            )  # добавляем для чистого вывода без индексов Pandas
    else:
        print(f"Текущие таблицы в схеме 'public': {tables}")


def main():

    data = load_data()
    data_after_processed = preprocess_data(data)

    print(data_after_processed.info())

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_root_base}",  # noqa
        pool_recycle=3600,
        # echo=True,
    )

    table_name = db_name_table


    with engine.begin() as conn:
        data_after_processed.to_sql(
            name=table_name,
            con=conn,
            schema="public",
            if_exists="replace",
            index=False,
        )

    check_table_and_data(engine, table_name)

if __name__ == "__main__":
    main()
