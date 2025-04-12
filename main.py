import requests
from datetime import datetime, timedelta


def fetch_api_hh():
    date_from = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    languages = "python OR javascript OR typescript OR java OR c#"
    payload = {
        'text': languages,
        'area': 1,
        'date_from': date_from
    }

    url = 'https://api.hh.ru/vacancies'

    # Выполняем GET-запрос с параметрами
    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()
    print(data)


# Пример вызова функции
if __name__ == "__main__":
    fetch_api_hh()