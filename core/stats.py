def calculate_vacancy_statistics(prepared_vacancies) -> dict[str, dict]:
    stats = {}

    for language, vacancy_data in prepared_vacancies.items():
        found = vacancy_data.get("found")
        salaries = vacancy_data.get("salaries", [])

        valid_salaries = [salary for salary in salaries if salary]
        vacancies_processed = len(valid_salaries)
        average_salary = int(sum(valid_salaries) / vacancies_processed) if vacancies_processed else 0

        stats[language] = {
            "vacancies_found": found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }

    sorted_stats = dict(
        sorted(
            stats.items(),
            key=lambda item: item[1]["average_salary"],
            reverse=True
        )
    )
    return sorted_stats