from .extract import load_dataset_from_GD, load_data_from_xlsx
from .transform import data_after_transform
from .load import save_data_to_parquet, read_data_from_parquet, write_to_db
from .validate import (
    check_file_parquet,
    check_file_xlsx,
    validate_xlsx_data,
    validate_parquet_data,
)
from dotenv import load_dotenv
import os
import click

load_dotenv()

default_data_dir = os.getenv("ETL_DATA_DIR")
file_id = os.getenv("FILE_ID")
db_user = os.getenv("ETL_DB_USER")
db_password = os.getenv("ETL_DB_PASSWORD")
db_url = os.getenv("ETL_DB_URL")
db_port = os.getenv("ETL_DB_PORT")
db_root_base = os.getenv("ETL_DB_ROOT_BASE")
db_name_table = os.getenv("ETL_DB_NAME_TABLE")

assert db_user, "ETL_DB_USER не установлен в .env"
assert db_password, "ETL_DB_PASSWORD не установлен в .env"
assert db_url, "ETL_DB_URL не установлен в .env"
assert db_port, "ETL_DB_PORT не установлен в .env"
assert db_root_base, "ETL_DB_ROOT_BASE не установлен в .env"


@click.command()
@click.option(
    "--size-data-to-db",
    default=100,
    help="Количество строк для записи в БД (по умолчанию: 100)",
)
@click.option(
    "--xlsx-name", default="dataset", help="Название XLSX файла (без расширения)"
)
@click.option(
    "--parquet-name", default="dataset", help="Название Parquet файла (без расширения)"
)
@click.option(
    "--data-dir",
    default=default_data_dir,
    help="Директория для данных (по умолчанию из .env)",
)
@click.option("--no-write-db", is_flag=True, help="Не записывать в базу данных")
@click.option(
    "--force",
    is_flag=True,
    help="Принудительно перезаписать XLSX файл (скачать заново с Google Drive)",
)
def etl_pipeline(
    size_data_to_db, xlsx_name, parquet_name, data_dir, no_write_db, force
):
    """
    ETL пайплайн по обработке данных авто
    """

    click.echo(f"\n{'='*60}")
    click.echo("--ЗАПУСК ETL--")
    click.echo(f"{'='*60}\n")
    click.echo(f"Размер выборки для БД: {size_data_to_db}\n")
    click.echo(f"XLSX файл: {xlsx_name}.xlsx\n")
    click.echo(f"Parquet файл: {parquet_name}.parquet\n")
    click.echo(f"Директория данных: {data_dir}\n")
    click.echo(f"Запись в БД: {'НЕТ' if no_write_db else 'ДА'}\n")
    click.echo(f"Принудительная перезагрузка: {'ДА' if force else 'НЕТ'}\n")
    click.echo(f"{'='*60}\n")

    raw_dir = os.path.join(data_dir, "raw")
    processed_dir = os.path.join(data_dir, "processed")

    for directory in [data_dir, raw_dir, processed_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            click.echo(f"Директория создана -> {directory}")

    xlsx_filename = f"{xlsx_name}.xlsx"
    parquet_filename = f"{parquet_name}.parquet"
    xlsx_path = os.path.join(raw_dir, xlsx_filename)

    if force:
        if os.path.exists(xlsx_path):
            os.remove(xlsx_path)
            click.echo(f"Удален существующий XLSX файл: {xlsx_path}\n")
        else:
            click.echo(f"XLSX файл для удаления не найден\n")

    click.echo(f"\n{'='*60}")
    click.echo
    print("--ПРОВЕРКА НАЛИЧИЯ DATASET В ФОРМАТЕ .PARQUET В ДИРЕКТОРИИ data/processed--")
    click.echo(f"{'='*60}\n")

    data = None

    if check_file_parquet(processed_dir, parquet_filename):

        click.echo("Dataset в формате .parquet найден!")
        parquet_path = os.path.join(processed_dir, parquet_filename)
        data = read_data_from_parquet(parquet_path)

    else:
        click.echo("Dataset в формате .parquet не найден!")

        click.echo(f"\n{'=' * 60}")
        click.echo("--ПРОВЕРКА НАЛИЧИЯ DATASET В ФОРМАТЕ XLSX В ДИРЕКТОРИИ data/raw--")
        click.echo(f"{'=' * 60}\n")

        f_path = check_file_xlsx(raw_dir, xlsx_filename)

        if not f_path or force:
            click.echo("xlsx файл не найден. Скачиваем с Google Drive...")
            f_path = load_dataset_from_GD(raw_dir, file_id, xlsx_filename)
            click.echo(f"Файл загружен в {f_path}")
        else:
            print(f"xlsx файл найден в {f_path}")

        dirty_data = load_data_from_xlsx(f_path)

        click.echo("Валидация исходных данных...")
        validate_xlsx_data(dirty_data)

        click.echo("Выполняем преобразование сырых данных...")
        clean_data = data_after_transform(dirty_data)
        parquet_path = save_data_to_parquet(clean_data, processed_dir, parquet_filename)
        click.echo(f"Данные сохранены в {parquet_path}")
        data = read_data_from_parquet(parquet_path)

    if data is not None:
        click.echo("Валидация выходных данных...")
        valid = validate_parquet_data(data)
        assert valid, "ERROR IN .PARQUET FILE"

        if not no_write_db:
            click.echo("\nЗапись в базу данных...\n")
            data_into_db = write_to_db(
                data,
                db_user,
                db_url,
                db_password,
                db_port,
                db_root_base,
                db_name_table,
                size_data_to_db,
            )
            if not data_into_db:
                click.echo("Возникли проблемы при записи в БД")
        else:
            click.echo("\nЗапись в БД пропущена...")

        click.echo(f"\n{'='*60}")
        click.echo("--ETL УСПЕШНО ОКОНЧЕН -> ВЫВОД ДАННЫХ--")
        click.echo(f"{'='*60}\n")
        click.echo(data.info())
    else:
        click.echo("--ОШИБКА -> ДАННЫЕ НЕ БЫЛИ ЗАГРУЖЕНЫ ИЛИ ПРЕОБРАЗОВАНЫ")


if __name__ == "__main__":
    etl_pipeline()
