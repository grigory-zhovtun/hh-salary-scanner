from datetime import datetime, timedelta
import requests
import itertools
import time
from .settings import SJ_MOSCOW_ID, SJ_IT_PROGRAMMING_ID


def fetch_sj_vacancies(sj_key, languages, max_pages=None, per_page=100):
    base_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {"X-Api-App-Id": sj_key}
    vacancies_by_language = {lang: {"total": 0, "items": []} for lang in languages}

    for lang in languages:
        for page in itertools.count():
            if max_pages and page >= max_pages:
                break
            params = {
                "keyword": lang,
                "town": SJ_MOSCOW_ID,
                "catalogues": SJ_IT_PROGRAMMING_ID,
                "period": 30,
                "no_correction": 1,
                "page": page,
                "count": per_page,
                "order_field": "date",
                "order_direction": "desc",
            }
            resp = requests.get(base_url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            vacancy_page = resp.json()
            vacancies_by_language[lang]["total"] = vacancy_page.get("total", len(vacancies_by_language[lang]["items"]))
            vacancies_by_language[lang]["items"].extend(vacancy_page["objects"])
            if not vacancy_page["more"]:
                break
            time.sleep(0.3)
    return vacancies_by_language


def format_sj_vacancies(vacancies_by_language, predict_salary_fn):
    formatted = {}
    for language, vacancies_raw in vacancies_by_language.items():
        found = vacancies_raw["total"]
        vacancies = vacancies_raw["items"]
        vacs = [
            {
                "title": vacancy["profession"],
                "city": vacancy["town"]["title"],
                "salary": predict_salary_fn(vacancy),
                "currency": vacancy["currency"],
                "published": datetime.fromtimestamp(vacancy["date_published"]).strftime("%Y-%m-%d"),
            }
            for vacancy in vacancies
        ]
        formatted[language] = {"found": found, "vacancies": vacs}

    return formatted