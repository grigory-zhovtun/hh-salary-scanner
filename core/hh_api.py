from datetime import datetime, timedelta
import requests
import itertools
import time
from collections import defaultdict
from .settings import HH_MOSCOW_ID


def fetch_hh_vacancies(languages, max_pages=None, per_page=100):
    date_from = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    vacancies_by_language = defaultdict(lambda: {"found": 0, "items": []})

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
            response = requests.get("https://api.hh.ru/vacancies", params=params, timeout=10)
            response.raise_for_status()
            vacancy_page = response.json()

            lang_stats = vacancies_by_language[lang]
            lang_stats["items"].extend(vacancy_page["items"])
            lang_stats["found"] = vacancy_page["found"]

            if not vacancy_page["pages"] or page >= vacancy_page["pages"] - 1:
                break
            time.sleep(0.3)
    return dict(vacancies_by_language)
