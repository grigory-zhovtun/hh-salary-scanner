import requests
import argparse
import re
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


def fetch_api_hh(languages, page):
    date_from = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    payload = {
        'text': languages,
        'area': 1,
        'per_page': 100,
        'page': page,
        'date_from': date_from
    }

    url = 'https://api.hh.ru/vacancies'
    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()
    return data['items']


def grouped_vacancies_data(vacancies):
    languages = {
        "python": "Python",
        "javascript": "Javascript",
        "typescript": "Typescript",
        "java": "Java",
        "c#": "C#"
    }
    stats = {
        disp: {
            "vacancies_found": 0,
            "vacancies_processed": 0,
            "total_salary": 0.0
        }
        for disp in languages.values()
    }

    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in languages.keys()) + r')\b', flags=re.IGNORECASE)

    for vac in vacancies:
        text = " ".join([
            vac.get("name") or "",
            vac.get("snippet", {}).get("requirement") or "",
            vac.get("snippet", {}).get("responsibility") or ""
        ])
        found = {match.lower() for match in pattern.findall(text)}
        if not found:
            continue

        salary = predict_rub_salary(vac)
        for key in found:
            lang = languages[key]
            stats[lang]["vacancies_found"] += 1
            if salary is not None:
                stats[lang]["vacancies_processed"] += 1
                stats[lang]["total_salary"] += salary

    result = {}
    for lang, data in stats.items():
        proc = data["vacancies_processed"]
        avg = int(data["total_salary"] / proc) if proc > 0 else None
        result[lang] = {
            "vacancies_found": data["vacancies_found"],
            "vacancies_processed": proc,
            "average_salary": avg
        }
    return result


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

    all_vacancies = []
    for page in range(0, 20):
        all_vacancies.extend(fetch_api_hh(args.search, page))
    print(grouped_vacancies_data(all_vacancies))
    # grouped_vacancies_data(all_vacancies)


if __name__ == "__main__":
    main()