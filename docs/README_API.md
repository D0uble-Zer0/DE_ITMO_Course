<h1 id="header" align="center">
<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmoyYnBnamd3N3dobHBjMXB2NmljYWlpOXAwOW9iaWR2eHA0djRqYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YnTLgXn0zFXjbqF152/giphy.gif" width="30px"/>
  Subproject -> dataset load from API
  <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmoyYnBnamd3N3dobHBjMXB2NmljYWlpOXAwOW9iaWR2eHA0djRqYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YnTLgXn0zFXjbqF152/giphy.gif" width="30px"/>
</h1>

---

## Описание
_Подпроект_ является частью общего проекта, выполняемого в рамках курса **Инжиниринг управления данными** в университете
ИТМО.  
_Задачей_ подпроекта является нахождения интересующего нас API и выгрузка данных с него в dataset.csv и dataset.parquet для
дальнейшей обработки.
  
Вся основная информация о проекте представлены в файле [README.md](../README.md)

---

## Выбранный API

Ссылка на выбранный в подпроекте API - https://openbrewerydb.org/

Мы будем рассматривать и собирать данные по пивоварням, сидроварням, пивным барам и бутылочным цехам во всем мире.

---

## Ход работы

1) Прежде всего были обозначены идеи, которые закладывались в код проекта:
   1) Пользователь (разработчик) может сам **выбрать количество запрашиваемых у API пивоварен**.
   2) Далее, на 1 этапе, **мы должны загрузить** выбранное ранее количество пивоварен в переменную-словарь.
   3) Последним, 2 этапом, данные должны сохраниться в директорию data в формате .csv. Здесь происходит типизация данных.
   Также необходимо вывести информацию о dataset.
2) Для реализации первого подпункта с выбором количества запрашиваемых данных у API - был создан скрипт ``get_user_API.py``
3) Для реализации второго подпункта создался скрипт ``data_from_API.py``
4) Для реализации последнего подпункта создался скрипт ``data_saver_API.py``
5) В конце в основном файле ``API_example.py`` все скрипт были объединены и запущены.

**ВЫВОД В ТЕРМИНАЛЕ РАБОТЫ ПРОГРАММЫ**  
![img.png](../../docs/images/Result_1_part.png)
![img.png](../../docs/images/Result_2_part.png)