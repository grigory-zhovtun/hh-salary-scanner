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

    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()
    return data['items']


if __name__ == "__main__":
    all_vacancies = fetch_api_hh()

    count_vacancies = dict()
    for vacancy in all_vacancies:
        count_vacancies[vacancy['name']] = count_vacancies.get(vacancy['name'], 0) + 1

    for name, count in count_vacancies.items():
        print(f'{name}: {count}')