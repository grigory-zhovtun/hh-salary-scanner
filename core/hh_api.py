from datetime import datetime, timedelta
import requests
import itertools
import time


def fetch_api_hh(languages, max_pages=None, per_page=100):
    date_from = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    raw = {lang: [] for lang in languages}

    for lang in languages:
        for page in itertools.count():
            if max_pages and page >= max_pages:
                break
            params = {
                "text": lang,
                "area": 1,
                "per_page": per_page,
                "page": page,
                "date_from": date_from,
            }
            resp = requests.get("https://api.hh.ru/vacancies", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            raw[lang].extend(data["items"])
            if not data["pages"] or page >= data["pages"] - 1:
                break
            time.sleep(0.3)
    return raw


def format_hh_vacancies(raw, predict_salary_fn):
    formatted = {}
    for lang, vacs in raw.items():
        formatted[lang] = [
            {
                "title": v.get("name"),
                "city": v.get("area", {}).get("name"),
                "salary": predict_salary_fn(v),
                "currency": (v.get("salary") or {}).get("currency"),
                "published": (v.get("published_at") or "")[:10],
            }
            for v in vacs
        ]
    return formatted
