"""
Данный код был создан с использованием нейросетей. Дальнейшая работа с ним вне раздела
tests будет выполняться без использования нейросетей.
"""

# Импортируем нужные библиотеки
import requests  # для общения с API
from tqdm import tqdm  # для красивого прогресс-бара
import pandas as pd  # для работы с таблицами
import time  # для добавления задержек между запросами

# Настраиваем константы
API_URL = "https://api.openbrewerydb.org/v1/breweries"
OUTPUT_FILENAME = "data/breweries_500.csv"  # новое имя файла для 500 пивоварен


def load_data_from_api(api_url: str, total_items: int = 500) -> list[dict]:
    """
    Загружаем данные из веб-API

    Для 500 пивоварен нам нужно:
    - Делать несколько запросов (пагинация)
    - Быть вежливыми к серверу (добавлять задержки)
    - Обрабатывать возможные ошибки
    """
    all_breweries = []  # здесь будем хранить все пивоварни

    # Настраиваем пагинацию - будем запрашивать по 50 пивоварен за раз
    per_page = 50  # максимальное количество на одну страницу
    # Вычисляем сколько страниц нужно для 500 пивоварен
    pages_needed = (total_items + per_page - 1) // per_page

    print(f"Загружаем {total_items} пивоварен...")
    print(f"Это займет примерно {pages_needed} запросов к API")

    # Проходим по всем нужным страницам
    for page in tqdm(range(1, pages_needed + 1)):
        # Считаем сколько еще нужно загрузить
        items_remaining = total_items - len(all_breweries)
        # На текущей странице берем либо максимум (50), либо остаток
        current_per_page = min(per_page, items_remaining)

        # Если уже загрузили достаточно - выходим
        if current_per_page <= 0:
            break

        # Подготавливаем параметры запроса
        params = {
            "page": page,  # номер текущей страницы
            "per_page": current_per_page,  # сколько элементов на этой странице
        }

        try:
            # Отправляем запрос к API
            response = requests.get(
                api_url,
                params=params,
                headers={"Content-Type": "application/json"},
                timeout=15,  # увеличиваем таймаут для больших запросов
            )

            # Проверяем успешность запроса
            if response.status_code == 200:
                breweries = response.json()  # преобразуем JSON в Python-объекты

                # Если API вернуло пустой список - значит данные кончились
                if not breweries:
                    print(f"\nДостигнут конец данных на странице {page}")
                    break

                # Добавляем новые пивоварни в общий список
                all_breweries.extend(breweries)

                # Выводим отладочную информацию
                print(f"\nСтраница {page}: загружено {len(breweries)} пивоварен")
                print(f"Всего загружено: {len(all_breweries)} из {total_items}")

                # Проверяем условия для остановки:
                # 1. Уже загрузили достаточно
                # 2. На странице меньше данных чем мы запрашивали (значит данные кончились)
                if (
                    len(all_breweries) >= total_items
                    or len(breweries) < current_per_page
                ):
                    break

            else:
                # Обрабатываем ошибки API
                print(
                    f"\nОШИБКА! API вернуло статус {response.status_code} на странице {page}"
                )
                print(f"Текст ошибки: {response.text}")

                # Если это ошибка сервера (5xx), возможно стоит подождать
                if response.status_code >= 500:
                    print("Сервер перегружен, делаем паузу 10 секунд...")
                    time.sleep(10)
                else:
                    break  # для других ошибок прерываем загрузку

        except requests.exceptions.RequestException as e:
            # Обрабатываем сетевые ошибки
            print(f"\nСетевая ошибка на странице {page}: {e}")
            print("Делаем паузу 5 секунд и пробуем продолжить...")
            time.sleep(5)
            continue  # пробуем следующую страницу

        # Делаем небольшую паузу между запросами чтобы не перегружать API
        # Это важно когда мы делаем много запросов подряд!
        time.sleep(0.5)

    # Возвращаем результат (обрезаем если случайно взяли больше)
    final_result = all_breweries[:total_items]
    print(f"\n✅ Финальный результат: загружено {len(final_result)} пивоварен")
    return final_result


def convert_to_df_and_save(data: list[dict], fname: str) -> pd.DataFrame | None:
    """
    Преобразуем список словарей в таблицу и сохраняем в CSV
    """
    if not data:
        print("Нет данных для сохранения!")
        return None

    # Создаем DataFrame из нашего списка пивоварен
    df = pd.DataFrame(data)

    # Сохраняем в CSV файл
    df.to_csv(fname, index=False)

    print(f"✅ Данные сохранены в файл: {fname}")
    print(f"📊 Размер таблицы: {df.shape} (строки x столбцы)")

    return df


def analyze_dataset(df: pd.DataFrame):
    """
    Анализируем наш датасет - смотрим что у нас получилось
    """
    print("\n" + "=" * 50)
    print("📈 АНАЛИЗ ДАТАСЕТА")
    print("=" * 50)

    # Базовая информация о таблице
    print("\n1. ОСНОВНАЯ ИНФОРМАЦИЯ:")
    print(f"   - Всего записей: {len(df)}")
    print(f"   - Всего столбцов: {len(df.columns)}")

    # Смотрим на столбцы
    print("\n2. СТОЛБЦЫ В ДАТАСЕТЕ:")
    for i, column in enumerate(df.columns, 1):
        print(f"   {i}. {column}")

    # Статистика по географическим данным
    print("\n3. ГЕОГРАФИЧЕСКАЯ СТАТИСТИКА:")
    if "state" in df.columns:
        state_counts = df["state"].value_counts()
        print(f"   - Штатов представлено: {len(state_counts)}")
        print(f"   - Топ-5 штатов по количеству пивоварен:")
        for state, count in state_counts.head().items():
            print(f"     • {state}: {count} пивоварен")

    if "country" in df.columns:
        country_counts = df["country"].value_counts()
        print(f"   - Стран представлено: {len(country_counts)}")

    # Показываем несколько примеров
    print("\n4. ПЕРВЫЕ 5 ПИВОВАРЕН:")
    display_columns = ["name", "city", "state", "country"]
    available_columns = [col for col in display_columns if col in df.columns]
    if available_columns:
        print(df[available_columns].head())


def main():
    """
    Главная функция - управляем всем процессом
    """
    # Создаем папку data если её нет
    import os

    os.makedirs("data", exist_ok=True)

    print("🚀 ЗАПУСК ПРОГРАММЫ ДЛЯ СОЗДАНИЯ ДАТАСЕТА ИЗ 500 ПИВОВАРЕН")
    print("=" * 60)

    # Шаг 1: Загружаем данные
    print("\n📍 ШАГ 1: Загрузка данных из API")
    breweries = load_data_from_api(API_URL, 500)

    # Проверяем успешность загрузки
    if not breweries:
        print("❌ Не удалось загрузить данные!")
        return

    # Шаг 2: Сохраняем в файл
    print("\n📍 ШАГ 2: Сохранение данных")
    result_df = convert_to_df_and_save(breweries, OUTPUT_FILENAME)

    if result_df is not None:
        # Шаг 3: Анализируем что получилось
        print("\n📍 ШАГ 3: Анализ данных")
        analyze_dataset(result_df)

        # Дополнительная информация
        print("\n🎉 ДАТАСЕТ УСПЕШНО СОЗДАН!")
        print(f"📁 Файл: {OUTPUT_FILENAME}")
        print(f"📊 Размер: {len(result_df)} пивоварен")
        print(f"🗂️ Столбцов: {len(result_df.columns)}")


# Запускаем программу если файл выполняется напрямую
if __name__ == "__main__":
    main()
