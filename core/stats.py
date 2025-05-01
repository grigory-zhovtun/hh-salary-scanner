def calculate_vacancy_statistics(vacancies) -> dict[str, dict]:
    stats = {}

    for language, vacancy_stats in vacancies.items():
        found = vacancy_stats.get("found")
        salaries = vacancy_stats.get("salaries", [])
        salaries = [salary for salary in salaries if salary is not None]

        stats[language] = {
            "vacancies_found": found,
            "vacancies_processed": len(salaries),
            "average_salary": (
                int(sum(salaries) / len(salaries))
                if salaries else 0
            ),
    }

    sorted_stats = dict(
        sorted(
            stats.items(),
            key=lambda item: item[1]["average_salary"],
            reverse=True
        )
    )
    return sorted_stats