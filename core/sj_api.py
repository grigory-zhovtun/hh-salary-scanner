from datetime import datetime, timedelta
import requests
import itertools
import time


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