# Приложение Python по выгрузке данных из Google Drive с конфигурацией пакетных менеджеров Conda+Poetry

---
**ПРИМЕЧАНИЕ** - проект является учебным в ходе обучения дисциплины "Инжиниринг управления данными".

---

## Требования:
 - [Conda >= 24.3.0](https://www.anaconda.com/docs/getting-started/miniconda/install)
 - [python >= 3.11.9](https://www.python.org/downloads/release/python-3119/)
 - [poetry >= 2.2.0](https://habr.com/ru/articles/593529/)
 - pip
---

**ПРИМЕЧАНИЕ** - инструкция по настройке в IDE PyCharm представлена ниже.

---

## Инструкция по установке Conda+Poetry и восстановления окружения

---
**ПРИМЕЧАНИЕ** - для восстановления окружения вам понадобятся 3 файла: *environment.yml*, *pyproject.toml* 
и *poetry.lock*
---

1) Создаем в PyCharm новый проект с любым выбранным interpreter.
2) После создания удаляем ВСЕ имеющиеся файлы в папке проекта.
3) Создаем внутри папки файл ```environment.yml``` в котором прописываем следующий минимум:
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
---

**ПРИМЕЧАНИЕ** - для восстановления проверьте установку Miniconda. И далее на основе готового файла *environment.yml*
повторите шаг №4

---
4) Открываем терминал в PyCharm и прописываем:  
`cоnda env create -f environment.yml`  
Затем прописываем:  
`cоnda activate <название вашего окружения>`
5) Ставим Poetry командой:  
`poetry init`  
---

**ПРИМЕЧАНИЕ** - все зависимости добавим позже командой `poetry add`

---
6) Для того чтобы *poetry* поставился в виртуальное окружение *conda*
прописываем:  
`poetry config virtualenvs.create false`
7) Прописываем `poetry install`

---

**ПРИМЕЧАНИЕ** - после восстановления из файла *environment.yml* повторите шаги №6-8

---
8) В PyCharm настраиваем interpreter выполняя команды:
    1) `Add local interpreter`
    2) `Conda environments`
    3) `use existing environment`
    4) `<название вашего окружения в выпадающем списке>`
---

## Скриншот с результатом команды raw_data.head(10)
![img_1.png](img_1.png)
   
