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

data = pd.read_parquet(
    r"data/data_car.parquet"
)  # ../ это означает подняться на директорию выше

pd.set_option("display.max_rows", 150)


new_column_names = {
    col: col.lower() for col in data.columns
}  # снижаем регистр всех букв в нижний
new_column_names["Have a leather interior?"] = "have_a_leather_interior"
new_column_names["Fuel type"] = "fuel_type"
new_column_names["Engine volume"] = "engine_volume"
new_column_names["Car have a left wheel?"] = "car_have_a_left_wheel"

data.rename(columns=new_column_names, inplace=True)

data_hundred = data.head(100)  # отделяем 100 строк из датасета для загрузки

print(f"\n{'-'*60}\n")
print(data.info())
print(f"{'-'*60}\n")
print(data_hundred.shape)


engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_root_base}",  # noqa
    pool_recycle=3600,
    # echo=True,
)

with engine.begin() as conn:
    data_hundred.to_sql(
        name="titov",
        con=conn,
        schema="public",
        if_exists="replace",
        index=False,
    )


inspector = inspect(engine)
tables = inspector.get_table_names(schema="public")
if "titov" in tables:
    print(f"Ваша таблица найдена!!!")  # для самопроверки
else:
    print(f"Текущие таблицы в схеме 'public': {tables}")

# print(f"Текущие таблицы в схеме 'public': {tables}")

"""
Для проверки считаем данные, что их 100
"""
with engine.begin() as conn:
    df_sample = pd.read_sql("SELECT * FROM public.titov LIMIT 100", con=conn)
    print(df_sample.to_string(index=False)) # добавляем для чистого вывода без индексов Pandas
