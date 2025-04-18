import os
import argparse
from dotenv import load_dotenv

from core.hh_api import fetch_api_hh, format_hh_vacancies
from core.sj_api import fetch_sj_vacancies, format_sj_vacancies
from core.salary import predict_rub_salary
from core.stats import grouped_vacancies_data
from core.printer import terminal_print


def main():
    load_dotenv()

    languages = ["Python", "JavaScript", "Typescript", "Java", "C#"]

    parser = argparse.ArgumentParser(description="fetch information from HH and SJ vacancies")
    parser.add_argument("--search", nargs="+", default=languages)
    args = parser.parse_args()
    query = " ".join(args.search) if isinstance(args.search, list) else args.search

    if query is not None:
        languages = query.split(" ")

    hh_raw = fetch_api_hh(languages)
    hh_vacancies = format_hh_vacancies(hh_raw, predict_rub_salary)
    hh_stats = grouped_vacancies_data(hh_vacancies, languages)
    terminal_print(hh_stats, "HeadHunter Moscow")

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies = format_sj_vacancies(fetch_sj_vacancies(sj_secret_key, languages), predict_rub_salary)
    sj_stats = grouped_vacancies_data(sj_vacancies, languages)
    terminal_print(sj_stats, "SuperJob Moscow")

if __name__ == "__main__":
    main()