import requests
import itertools
import os
import time
import argparse
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv


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
    return data['items'], data['pages']


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


def fetch_api_sj(sj_key, languages, max_pages=None, per_page=100):
    base_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": sj_key}
    vacancies, seen_ids = {lang: [] for lang in languages}, set()

    for lang in languages:
        for page in itertools.count():
            if max_pages and page >= max_pages:
                break
            params = {
                "keyword": lang,
                "town": 4,            # Москва
                "catalogues": 33,     # под‑каталог «Программисты»
                "period": 30,         # последний месяц
                "no_correction": 1,   # без автоисправлений
                "page": page,
                "count": per_page,
                "order_field": "date",
                "order_direction": "desc",
            }
            try:
                resp = requests.get(base_url, params=params, headers=headers, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                for vac in data["objects"]:
                    if vac["id"] in seen_ids:
                        continue
                    seen_ids.add(vac["id"])
                    vacancies[lang].append(
                        {
                            "title": vac["profession"],
                            "city": vac["town"]["title"],
                            "salary_from": vac["payment_from"] or None,
                            "salary_to": vac["payment_to"] or None,
                            "currency": vac["currency"],
                            "published": datetime.fromtimestamp(
                                vac["date_published"]).strftime("%Y‑%m‑%d"),
                        }
                    )
                if not data["more"]:
                    break
                time.sleep(0.3)
            except requests.exceptions.HTTPError:
                time.sleep(1)
    return vacancies


def main():
    load_dotenv()

    languages = [
        "Python",
        "JavaScript",
        "Typescript",
        "Java",
        "C#"
    ]
    parser = argparse.ArgumentParser(
        description="fetch information from HH vacancies"
    )
    parser.add_argument(
        "--search",
        nargs='+',
        default=" OR ".join(languages),
        )

    args = parser.parse_args()
    query = " ".join(args.search)

    all_vacancies = []
    page = 0
    max_page = 1
    # while page < max_page:
    #     vacancies, max_page = fetch_api_hh(query, page)
    #     page += 1
    #     all_vacancies.extend(vacancies)
    # print(grouped_vacancies_data(all_vacancies))

    sj_secret_key = os.environ['SJ_SECRET_KEY']

    for lang, v in fetch_api_sj(sj_secret_key, languages).items():
        print(lang, v)

if __name__ == "__main__":
    main()