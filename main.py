import os
import argparse
from dotenv import load_dotenv

from core.hh_api import fetch_hh_vacancies, format_hh_vacancies
from core.sj_api import fetch_sj_vacancies, format_sj_vacancies
from core.salary import predict_rub_salary
from core.stats import grouped_vacancies_data
from core.printer import terminal_print
from core.settings import LANGUAGES


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="fetch information from HH and SJ vacancies")
    parser.add_argument("--search", nargs="+", default=LANGUAGES)
    args = parser.parse_args()

    languages = args.search if args.search else LANGUAGES

    raw_hh_vacancies = fetch_hh_vacancies(languages)
    hh_vacancies = format_hh_vacancies(raw_hh_vacancies, predict_rub_salary)
    hh_stats = grouped_vacancies_data(hh_vacancies)
    terminal_print(hh_stats, "HeadHunter Moscow")

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies = format_sj_vacancies(fetch_sj_vacancies(sj_secret_key, languages), predict_rub_salary)
    sj_stats = grouped_vacancies_data(sj_vacancies)
    terminal_print(sj_stats, "SuperJob Moscow")

if __name__ == "__main__":
    main()