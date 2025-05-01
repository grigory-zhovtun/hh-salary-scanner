def prepare_vacancies_for_stats(vacancies_by_language, predict_salary_fn):
    prepared_stats = {}
    for language, vacancies_raw in vacancies_by_language.items():
        found = vacancies_raw.get("found", vacancies_raw.get("total", 0))
        vacancies = vacancies_raw.get("items", [])

        prepared_stats[language] = {
            "found": found,
            "salaries": [
                predict_salary_fn(vacancy)
                for vacancy in vacancies
            ]
        }

    return prepared_stats