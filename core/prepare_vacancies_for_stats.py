def prepare_vacancies_for_stats(vacancies_by_language, predict_salary_fn):
    formatted = {}
    for language, vacancies_raw in vacancies_by_language.items():
        found = vacancies_raw.get("found", vacancies_raw.get("total", 0))
        vacancies = vacancies_raw.get("items", [])

        vacs = [
            {
                "title": vacancy.get("name")       # HH: name
                         or vacancy.get("profession"),  # SJ: profession
                "salary": predict_salary_fn(vacancy),
            }
            for vacancy in vacancies
        ]

        formatted[language] = {
            "found": found,
            "vacancies": vacs
        }

    return formatted