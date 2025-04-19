def calculate_vacancy_statistics(vacancies) -> dict[str, dict]:
    stats = {}

    for lang, info in vacancies.items():
        found = info.get("found")
        vacs = info.get("vacancies", [])
        salaries = [v["salary"] for v in vacs if v["salary"] is not None]

        stats[lang] = {
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