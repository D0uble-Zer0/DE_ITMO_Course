import pandas as pd
import os
from sqlalchemy import create_engine, inspect, text
import psycopg2


def save_data_to_parquet(data, processed_dir, filename):
    """
    Сохраняем dataset в .parquet
    """

    f_path = os.path.join(processed_dir, filename)
    data.to_parquet(f_path, index=False)
    return f_path


def read_data_from_parquet(file_path):
    """
    Загружаем данные из .parquet
    """
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    else:
        raise FileNotFoundError("Ошибка чтения файла .parquet")


def write_to_db(data, user, url, password, port, root_base, name_table, size):
    """
    Записываем данные в PostgreSQL базу данных
    """

    print(f"\n{'='*60}")
    print("--Загрузка в БД после преобразований--")
    print(f"{'='*60}\n")

    data_into_db = data.head(size)

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{url}:{port}/{root_base}",
        pool_recycle=3600,
    )

    try:
        with engine.begin() as conn:
            data_into_db.to_sql(
                name=name_table,
                con=conn,
                schema="public",
                if_exists="replace",
                index=False,
            )
        print(
            f"Данные записаны в таблицу {name_table}, количество строк {len(data_into_db)}"
        )
    except Exception as e:
        print(f"Ошибка - {e}")
        return False

    try:
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE public.{name_table} ADD PRIMARY KEY (id)"))
        print("Первичный ключ успешно добавлен!")
    except Exception as e:
        print(f"Ошибка - {e}")

    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema="public")

        if name_table in tables:
            print(f"Таблица {name_table} успешно найдена!\n")
            # print(f"Текущие таблицы в схеме 'public': {tables}\n")
            print(f"Выводим первые 5 строк...\n")

            with engine.begin() as conn:
                data_test = pd.read_sql(
                    f"SELECT * FROM public.{name_table} LIMIT 5", con=conn
                )
                print(data_test.to_string(index=False))
        else:
            print(f"Таблица {name_table} не найдена!\n")
            print(f"Текущие таблицы в схеме 'public': {tables}")
            return False
    except Exception as e:
        print(f"Ошибка - {e}")
        return False

    return True
