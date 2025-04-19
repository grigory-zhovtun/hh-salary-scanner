from datetime import datetime, timedelta
import requests
import itertools
import time
from .settings import HH_MOSCOW_ID


def fetch_hh_vacancies(languages, max_pages=None, per_page=100):
    date_from = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    vacancies_by_language = {lang: {"found": 0, "items": []} for lang in languages}

    for lang in languages:
        for page in itertools.count():
            if max_pages and page >= max_pages:
                break
            params = {
                "text": lang,
                "area": HH_MOSCOW_ID,
                "per_page": per_page,
                "page": page,
                "date_from": date_from,
            }
            resp = requests.get("https://api.hh.ru/vacancies", params=params, timeout=10)
            resp.raise_for_status()
            vacancy_page = resp.json()
            vacancies_by_language[lang]["found"] = vacancy_page.get("found", len(vacancies_by_language[lang]["items"]))
            vacancies_by_language[lang]["items"].extend(vacancy_page["items"])
            if not vacancy_page["pages"] or page >= vacancy_page["pages"] - 1:
                break
            time.sleep(0.3)
    return vacancies_by_language
