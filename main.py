import requests
import itertools
import os
import time
import argparse
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv


def predict_rub_salary(vacancy):
    # извлекаем данные о зарплате независимо от структуры
    if isinstance(vacancy.get("salary"), dict):
        pay_from = vacancy["salary"].get("from")
        pay_to = vacancy["salary"].get("to")
        currency = vacancy["salary"].get("currency")
    else:
        pay_from = vacancy.get("payment_from")
        pay_to = vacancy.get("payment_to")
        currency = vacancy.get("currency")

    pay_from = None if not pay_from else pay_from
    pay_to = None if not pay_to else pay_to
    if not currency or currency.lower() not in ("rur", "rub"):
        return None

    if pay_from is not None and pay_to is not None:
        return (pay_from + pay_to) / 2
    if pay_from is not None:
        return pay_from * 1.2
    if pay_to is not None:
        return pay_to * 0.8
    return None


def fetch_api_hh(query, max_pages=None, per_page=100):
    date_from = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    items = []

    for page in itertools.count():
        if max_pages and page >= max_pages:
            break

        params = {
            "text": query,
            "area": 1,
            "per_page": per_page,
            "page": page,
            "date_from": date_from,
        }
        resp = requests.get("https://api.hh.ru/vacancies", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        items.extend(data["items"])
        if not page < data["pages"] - 1:
            break

        time.sleep(0.3)

    return items


def format_hh_vacancies(vacancies, predict_salary_fn):
    lang_map = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "Typescript",
        "java": "Java",
        "c#": "C#",
    }
    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in lang_map) + r')\b', flags=re.IGNORECASE)
    formatted = {v: [] for v in lang_map.values()}

    for v in vacancies:
        text = " ".join([
            v.get("name") or "",
            v.get("snippet", {}).get("requirement") or "",
            v.get("snippet", {}).get("responsibility") or "",
        ])
        langs = {m.lower() for m in pattern.findall(text)}
        if not langs:
            continue

        vacancy_common = {
            "title": v.get("name"),
            "city": v.get("area", {}).get("name"),
            "salary": predict_salary_fn(v),
            "currency": (v.get("salary") or {}).get("currency"),
            "published": (v.get("published_at") or "")[:10],
        }

        for l in langs:
            formatted[lang_map[l]].append(vacancy_common)

    return formatted


def grouped_vacancies_data(vacancies: dict[str, list[dict]],
                           languages: list[str]) -> dict[str, dict]:
    stats = {
        lang: {
            "vacancies_found": 0,
            "vacancies_processed": 0,
            "average_salary": 0.0,
        }
        for lang in languages
    }

    for lang in languages:
        lang_vacs = vacancies.get(lang, [])
        salaries = [v["salary"] for v in lang_vacs if v["salary"] is not None]

        stats[lang]["vacancies_found"] = len(lang_vacs)
        stats[lang]["vacancies_processed"] = len(salaries)
        stats[lang]["average_salary"] = (
            sum(salaries) / len(salaries) if salaries else 0.0
        )

    return stats


def fetch_sj_vacancies(sj_key, languages, max_pages=None, per_page=100):
    base_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": sj_key}
    raw = {lang: [] for lang in languages}

    for lang in languages:
        for page in itertools.count():
            if max_pages and page >= max_pages:
                break
            params = {
                "keyword": lang,
                "town": 4,
                "catalogues": 33,
                "period": 30,
                "no_correction": 1,
                "page": page,
                "count": per_page,
                "order_field": "date",
                "order_direction": "desc",
            }
            resp = requests.get(base_url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            raw[lang].extend(data["objects"])
            if not data["more"]:
                break
            time.sleep(0.3)
    return raw


def format_sj_vacancies(raw, predict_salary_fn):
    formatted = {}
    for lang, vacs in raw.items():
        formatted[lang] = [
            {
                "title": v["profession"],
                "city": v["town"]["title"],
                "salary": predict_salary_fn(v),
                "currency": v["currency"],
                "published": datetime.fromtimestamp(v["date_published"]).strftime("%Y-%m-%d"),
            }
            for v in vacs
        ]
    return formatted


def main():
    load_dotenv()

    languages = ["Python", "JavaScript", "Typescript", "Java", "C#"]

    parser = argparse.ArgumentParser(description="fetch information from HH and SJ vacancies")
    parser.add_argument("--search", nargs="+", default=" OR ".join(languages))
    args = parser.parse_args()
    query = " ".join(args.search) if isinstance(args.search, list) else args.search

    hh_vacancies_raw = fetch_api_hh(query)
    hh_vacancies = format_hh_vacancies(hh_vacancies_raw, predict_rub_salary)
    print(grouped_vacancies_data(hh_vacancies, languages))

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies = format_sj_vacancies(fetch_sj_vacancies(sj_secret_key, languages), predict_rub_salary)
    print(grouped_vacancies_data(sj_vacancies, languages))

if __name__ == "__main__":
    main()