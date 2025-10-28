import os


def check_file_parquet(data_dir, filename="dataset.parquet"):
    """
    Проверка в директории data dataset.parquet
    """
    file_path = os.path.join(data_dir, filename)
    return os.path.exists(file_path)

def check_file_xlsx(data_dir, filename="dataset.xlsx"):
    """
    Проверка в директории data dataset.xlsx
    """
    file_path = os.path.join(data_dir, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        return False
