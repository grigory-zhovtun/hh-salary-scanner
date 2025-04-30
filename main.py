import os
import argparse
from dotenv import load_dotenv

from core.hh_api import fetch_hh_vacancies
from core.sj_api import fetch_sj_vacancies
from core.format_vacancies import format_vacancies
from core.salary import predict_rub_salary
from core.stats import calculate_vacancy_statistics
from core.printer import print_statistics_table
from core.settings import LANGUAGES


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="fetch information from HH and SJ vacancies")
    parser.add_argument("--search", nargs="+", default=LANGUAGES)
    args = parser.parse_args()

    languages = args.search if args.search else LANGUAGES

    unformatted_hh_vacancies = fetch_hh_vacancies(languages)
    hh_vacancies = format_vacancies(unformatted_hh_vacancies, predict_rub_salary)
    hh_stats = calculate_vacancy_statistics(hh_vacancies)
    print_statistics_table(hh_stats, "HeadHunter Moscow")

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies = format_vacancies(fetch_sj_vacancies(sj_secret_key, languages), predict_rub_salary)
    sj_stats = calculate_vacancy_statistics(sj_vacancies)
    print_statistics_table(sj_stats, "SuperJob Moscow")

if __name__ == "__main__":
    main()