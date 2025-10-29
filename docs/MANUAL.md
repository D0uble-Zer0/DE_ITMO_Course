<h1 id="header" align="center">
  Manual for data engineering project
</h1>

>[!NOTE]
>*Данная инструкция создана для проекта по анализу данных по ценам проданных автомобилей.*

---

## Настройка Conda+Poetry

>[!IMPORTANT]
> На вашем компьютере глобально должны быть предустановленны [Conda](https://www.anaconda.com/docs/getting-started/miniconda/install) и [Poetry](https://habr.com/ru/articles/593529/)

>[!NOTE]
> Инструкция может использоваться для настройки в IDE - Pycharm и Visual Studio Code.

1) Создаем в новый проект.
2) Создаем внутри папки файл ```environment.yml``` в котором прописываем следующий минимум:
    ```
   name: <название вашего окружения>
   channels:
    - conda-forge # канал с актуальными
    пакетами.
    - defaults
   dependencies:
    - python = <ваша версия python>
    - poetry = <ваша версия poetry>
    - pip # для работы poetry внутри conda
   ```

3) Открываем терминал и прописываем:  
`conda env create -f environment.yml`    
`cоnda activate <название вашего окружения>`
4) Ставим Poetry командой:  
`poetry init`
  
  
>[!NOTE]
> Все зависимости добавим позже командой `poetry add`
  
  
5) Для того чтобы *poetry* поставился в виртуальное окружение *conda*
прописываем:  
`poetry config virtualenvs.create false`
6) Прописываем  
`poetry install`

## Восстановление окружения 

>[!IMPORTANT]
> Для восстановления окружения вам понадобятся 2 файла: `environment.yml`, `pyproject.toml`.

1) Проверяем установку Miniconda (при запуске в терминале перед путем папки должно быть слово (base))
2) Прописываем команды:  
`cоnda env create -f environment.yml`  
`cоnda activate <название вашего окружения>`
3) После восстановления окружения из файла *environment.yml* прописываем последовательно следующие команды:  
`poetry config virtualenvs.create false`
`poetry install`

---

Возврат в [README.md](../README.md)

---