<h1 id="header" align="center">
  Data Engineering project
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDM1em52YzFydjZzOHFtejdiZThkOGlscjhkcTJ1MDE4a3I4YnJoayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/7JQkl8JRJZbt8PZSio/giphy.gif" width="40px"/>
</h1>

> [!NOTE]
> *Перед проектом поставлена задача проведения анализа данных и нахождения зависимостей между ценой и признаком автомобиля.*

<div id="header" align="center">
  <img src="https://media2.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZDk2eWdyMTh0emVuZWJocXQwY2Iwc2ViMHFrdHc2YXdwODB2NjQwaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QpVUMRUJGokfqXyfa1/200.webp" width="400"/>
</div>

---

## Описание

<ins>Цели проекта</ins>:

- провести работу над данными;
- найти зависимости между ценой и признаками автомобиля;
- получить знания и опыт в области инжиниринга данными (Data Engineering).

<div>
  Разработка программ работы с базой данных ведется <ins>на языке Python</ins>.
  <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXQ5b2Zla2hvb2MwYXkxN3Ywcjhmd2xkYjh6MGd0ZTdmaHl2MTh6OCZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/LMt9638dO8dftAjtco/200.webp" width="15px"/>
</div>

## Этапы проекта

- [x] Создание репозитория проекта и поиск dataset.
- [x] Выгрузка Dataset c Google Drive c помощью `data_loader.py` и настройка окружения.
- [x] Выполнение приведения типов над dataset и сохранение его в формате `.parquet`.
- [x] Создание [подпроекта](docs/README_API.md) c целью выгрузки данных в dataset с API.
- [x] Создание [подпроекта](docs/README_Scrap.md) с целью сбора данных для dataset с помощью скраппинга.
- [x] Проведение EDA над dataset, используя технологию jupiter notebook.
- [x] Работа с базами данных SQLite и PostgreSQL.
- [x] Добавление визуализации в `EDA.ipynb`.
- [х] Создание `ETL`.

## Cсылки на dataset

Прямая ссылка на dataset - https://www.kaggle.com/datasets/deepcontractor/car-price-prediction-challenge?resource=download
\
Ссылка на сохраненный dataset - https://docs.google.com/spreadsheets/d/1PMhtD3LqyCzlZMEh-8aDPxre0wPw8v0U/edit?usp=drive_link&ouid=100105970921534140705&rtpof=true&sd=true

---

## Выгрузка Dataset c Google Drive c помощью `data_loader.py` и настройка окружения

>[!IMPORTANT]
> На вашем компьютере глобально должны быть предустановленны [Conda](https://www.anaconda.com/docs/getting-started/miniconda/install) и [Poetry](https://habr.com/ru/articles/593529/)

### Требования проекта:

 - [Conda >= 24.3.0](https://www.anaconda.com/docs/getting-started/miniconda/install)
 - [python >= 3.11.9](https://www.python.org/downloads/release/python-3119/)
 - [poetry >= 2.2.0](https://habr.com/ru/articles/593529/)
 - pip

### Инструкция по установке Conda+Poetry

>[!IMPORTANT]
> Вся инструкция по установке и первичной настройке находится в файле [MANUAL.md](docs/MANUAL.md).

---

### Скриншот с результатом команды raw_data.head(10)

![img_1.png](docs/images/Screenshot_raw_data.png)

---

## Привидение типов данных и сохранение dataset в формате .parquet

>[!IMPORTANT]
> Программа выполняется запуском файла `main.py`.

После запуска скрипта получаем таблицу c исходными типами данных:  

```
 #   Column           Dtype  
---  ------           -----  
 0   ID               int64  
 1   Price            int64  
 2   Levy             object 
 3   Manufacturer     object 
 4   Model            object 
 5   Prod. year       int64  
 6   Category         object 
 7   Leather interior object 
 8   Fuel type        object 
 9   Engine volume    object 
 10  Mileage          object 
 11  Cylinders        float64
 12  Gear box type    object 
 13  Drive wheels     object 
 14  Doors            object 
 15  Wheel            object 
 16  Color            object 
 17  Airbags          int64  

   ```
 **Общая занимаемая память - 2.6 МB**

---

После используя таблицу:

![img.png](docs/images/table_of_types.png)

исправляем типы данных (скрипт `data_conversion.py`) и выводим их:  
```
 #   Column                      Dtype  
---  ------                      -----  
 0   ID                          int32  
 1   Price                       int32  
 2   Levy                        Int16 
 3   Manufacturer                category 
 4   Model                       category 
 5   Prod. year                  int8  
 6   Category                    category 
 7   Have a leather interior?    bool 
 8   Fuel type                   category 
 9   Engine volume               object 
 10  Mileage                     int32 
 11  Cylinders                   int8
 12  Gear box type               category 
 13  Drive wheels                category 
 14  Doors                       category 
 15  Car have a left wheel?      bool 
 16  Color                       category 
 17  Airbags                     int8  

   ```

---

>[!IMPORTANT]
> В вашем виртуальном окружении должна быть установлена зависимость _pyarrow_.

Сохранение dataset в формате `.parquet` происходит с помощью скрипта `data_saver.py`.

**Итогом** является уменьшение используемой памяти с **2.6 MB до 776.6 КB**

В дальнейшем все процедуры будут проводиться с файлом `.parquet`.

---

## Создание dataset из публичного API

>[!NOTE]
> Работа программы была описана в вложенном в директории API файле [README.md](docs/README_API.md)

---

## Создание dataset с помощью парсинга сайта

>[!NOTE]
> Работа программы была описана в вложенном в директории Scrapping файле [README.md](docs/README_Scrap.md).  
> Также для работы необходима установленная библиотека _BeautifulSoup4_.

---

## EDA над dataset

>[!IMPORTANT]
>Необходимо установить расширение _Jupyter Notebook_.

Весь процесс анализа и работы с данными в <ins>входном анализе данных (EDA)</ins> представлен в файле [EDA.ipynb](notebooks/EDA.ipynb).

---

## Работа с SQL базами данных

>[!IMPORTANT]
> В вашем виртуальном окружении должны быть установлены зависимости _sqlalchemy_ и _psycopg2_.

Работа в данной части проекта подразумевала поиск таблицы access в .db типа SQLite.  
После чего с найденными учетными данными происходило подключение, описанное в файле `write_to_db.py`, к удаленной БД типа PostgreSQL. Уже туда заносились 100 строк данных выбранного в проекте датасета.

---

## Работа с визуализацией.

>[!IMPORTANT]
> В вашем виртуальном окружении должны быть установлены зависимости _plotly_ и _statsmodels_.


Данная часть проекта подразумевает работу с визуализацией в файле `EDA.ipynb`.  
Поэтому в файле _jupyter notebook_ были добавлены дополнительные динамические графики и подпункты анализа.  
Из примеров:  
![img.png](docs/images/Test_plot.png)

**Основными критериями в данной пункте являлись:**
- Единый кастомный стиль
- Обязательно включить в работу график в виде сетки (несколько-в-одном)


Но так как выбранная библиотека _plotly_ имеет в себе элементы _JavaScript_, то Github не пропускает и не отображает корректно графики. Сделано это в целях безопасности.  
Поэтому с помощью команды:

```
jupyter nbconvert --to html <путь к файлу .ipynb>
```
был создан файл html.

Полная версия EDA с рабочими графиками _plotly_ представлена в [файле html](notebooks/EDA.html)

---

## Создание ETL процесса

Теперь имея все знания и компетенции необходимо выполнить создание **ETL pipeline**.

>[!NOTE]
>ETL - аббревиатура от **extract, transform, load**

### Структура ETL

```
Car-price-analysis-DE_project/
|
├── src/
|   ├──etl/
│      ├── __init__.py
│      ├── extract.py     # Extract from GDrive
│      ├── load.py
│      ├── main.py
|      ├── transform.py
│      └── validate.py
```

### Описание компонентов ETL

- `etl/extract.py`:
- `etl/load.py`:
- `etl/main.py`:
- `etl/transform.py`:
- `etl/validate.py`:




