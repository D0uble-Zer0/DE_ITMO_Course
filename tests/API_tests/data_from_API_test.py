import requests
from tqdm import tqdm
import time

API_URL = "https://api.openbrewerydb.org/v1/breweries"


def download_data(total_items: int) -> list[dict]:
    """
    Загружает данные из API
    """

    all_breweries = []
    per_page = 50  # количество items на 1 странице (пагинация)
    all_pages = (total_items + per_page - 1) // per_page

    print(f"\n Загружаем {total_items} пивоварен. Это займет {all_pages} запросов")

    for page in tqdm(range(1, all_pages + 1), desc="Загрузка"):
        items_remaining = total_items - len(all_breweries)  # осталось выгрузить
        current_per_page = min(
            per_page, items_remaining
        )  # не берем больше запрошенного количества пивоварен

        if current_per_page <= 0:
            break

        params = {"page": page, "per_page": current_per_page}

        try:
            response = requests.get(
                API_URL,
                params=params,
                headers={"Content-Type": "application/json"},
                timeout=20,
            )

            if response.status_code == 200:
                breweries = response.json()

                if not breweries:
                    break

                all_breweries.extend(
                    breweries
                )  # к списку all_breweries добавляется список breweries

                if (
                    len(all_breweries) >= total_items
                    or len(breweries) < current_per_page
                ):
                    break

            else:
                print(f"\nОШИБКА API: статус {response.status_code} на странице {page}")
                if response.status_code >= 500:  # перегрузка сервера/API
                    time.sleep(100)
                else:
                    break

        except requests.exceptions.RequestException:
            break

        time.sleep(0.5)

    result = all_breweries[:total_items]
    print(f"\nЗагружено {len(result)} пивоварен")
    return result
