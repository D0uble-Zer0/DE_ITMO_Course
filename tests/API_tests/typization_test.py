import pandas as pd

f_path = "data/breweries.csv"

data = pd.read_csv(f_path)


# print(data.dtypes)
data["brewery_type"] = data["brewery_type"].astype("category")
data["city"] = data["city"].astype("category")
data["state_province"] = data["state_province"].astype("category")
data["country"] = data["country"].astype("category")
data["state"] = data["state"].astype("category")
print(data.dtypes)
print(data["street"].value_counts())
