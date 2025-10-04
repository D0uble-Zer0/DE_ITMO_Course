from bs4 import BeautifulSoup
import requests
from create_table_test import population_table
from typification_data_test import create_save_dataset

SOURSE = "https://www.worldometers.info/world-population/"

headers = {
    "User-Agent": "Mozilla/5.0 (Educational Project; data will not be used for commercial or harmful purposes)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

r = requests.get(SOURSE, headers=headers)
r.raise_for_status()
r.encoding = "utf-8"

soup = BeautifulSoup(r.text, "html.parser")
table = soup.find("table", class_="datatable")

head_table, data = population_table(table)

dataset = create_save_dataset(head_table, data)

print(dataset.info())
