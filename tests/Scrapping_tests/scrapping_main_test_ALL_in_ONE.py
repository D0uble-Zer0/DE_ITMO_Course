from bs4 import BeautifulSoup
import os
import pandas as pd
import requests

SOURSE = "https://www.worldometers.info/world-population/"

headers = {
    "User-Agent": "Mozilla/5.0 (Educational Project; data will not be used for commercial or harmful purposes)"
    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

r = requests.get(SOURSE, headers=headers)
r.raise_for_status()

r.encoding = "utf-8"
# print(len(r.text))

soup = BeautifulSoup(r.text, "html.parser")
# print(soup)
table = soup.find("table", class_="datatable")
# print(table)

head_table = []
for th in table.find("thead").find_all("th"):
    span = th.find("span")
    if span:
        head_table.append(span.text.strip())
    else:
        head_table.append(th.text.strip())
# print(head_table)

data = []
for row in table.find("tbody").find_all("tr"):
    row_data = []
    for cell in row.find_all("td"):
        if cell.has_attr("data-order"):
            row_data.append(cell["data-order"])
        else:
            row_data.append(cell.text.strip())
    data.append(row_data)

# print(data)
dataset = pd.DataFrame(data, columns=head_table)

os.makedirs("data", exist_ok=True)

csv_path = "data/world_population.csv"
dataset.to_csv(csv_path, index=False, encoding="utf-8")
"""
pd.set_option("display.max_columns", None)  # Показать все колонки
pd.set_option("display.width", None)  # Не ограничивать ширину вывода
pd.set_option("display.max_colwidth", None)  # Не обрезать содержимое колонок
print(dataset)
"""


dataset["Year (July 1)"] = dataset["Year (July 1)"].astype(int)
dataset["Population"] = dataset["Population"].astype("int64")
dataset["Yearly % Change"] = dataset["Yearly % Change"].astype(float) / 100
dataset["Yearly Change"] = dataset["Yearly Change"].astype(float)
dataset["Median Age"] = dataset["Median Age"].astype(float) / 10000
dataset["Fertility Rate"] = dataset["Fertility Rate"].astype(float) / 10000
dataset["Density (P/Km²)"] = dataset["Density (P/Km²)"].astype(float)

# print(dataset)

parquet_path = "data/world_population.parquet"
dataset.to_parquet(parquet_path, index=False)

print(dataset.info())
