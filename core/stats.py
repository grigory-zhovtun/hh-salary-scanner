def grouped_vacancies_data(vacancies: dict[str, list[dict]],
                           languages: list[str]) -> dict[str, dict]:
    stats = {
        lang: {
            "vacancies_found": 0,
            "vacancies_processed": 0,
            "average_salary": 0,
        }
        for lang in languages
    }

    for lang in languages:
        lang_vacs = vacancies.get(lang, [])
        salaries = [v["salary"] for v in lang_vacs if v["salary"] is not None]

        stats[lang]["vacancies_found"] = len(lang_vacs)
        stats[lang]["vacancies_processed"] = len(salaries)
        stats[lang]["average_salary"] = (
            int(sum(salaries) / len(salaries))
            if salaries else 0
        )

    return stats