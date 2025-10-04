from bs4 import BeautifulSoup
import requests
from create_table import population_table
from typification_data import create_save_dataset

SOURSE = "https://www.worldometers.info/world-population/"

headers = {
    "User-Agent": "Mozilla/5.0 (Educational Project; data will not be used for commercial or harmful purposes)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}  # то, как нас видит сайт

r = requests.get(SOURSE, headers=headers)  # отправляем запрос сайту
r.raise_for_status()
r.encoding = "utf-8"  # для дальнейшей обработки необходимо указать точную кодировку

soup = BeautifulSoup(r.text, "html.parser")
table = soup.find(
    "table", class_="datatable"
)  # находим на странице нужную нам таблицу по маркерам

head_table, data = population_table(table)

dataset = create_save_dataset(head_table, data)

print(dataset.info())
