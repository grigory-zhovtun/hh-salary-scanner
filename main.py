import requests
import argparse
from datetime import datetime, timedelta


def predict_rub_salary(vacancy):
    if not vacancy['salary'] or vacancy['salary'].get('currency') != 'RUR':
        return None

    salary_from = vacancy['salary'].get('from')
    salary_to = vacancy['salary'].get('to')

    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2

    if salary_from is not None:
        return salary_from * 1.2

    if salary_to is not None:
        return salary_to * 0.8

    return None


def fetch_api_hh(languages):
    date_from = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
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


def main():
    languages = "python OR javascript OR typescript OR java OR c#"
    parser = argparse.ArgumentParser(
        description="fetch information from HH vacancies"
    )
    parser.add_argument(
        "--search",
        type=str,
        default=languages)

    args = parser.parse_args()

    all_vacancies = fetch_api_hh(args.search)

    count_vacancies = dict()
    for vacancy in all_vacancies:
        count_vacancies[vacancy['name']] = count_vacancies.get(vacancy['name'], 0) + 1

    for name, count in count_vacancies.items():
        print(f'{name}: {count}')

    for vacancy in all_vacancies:
        if vacancy:
            print(predict_rub_salary(vacancy))

if __name__ == "__main__":
    main()