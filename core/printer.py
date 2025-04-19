from terminaltables import AsciiTable


def terminal_print(stats_by_language, title):
    headers = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language in stats_by_language:
        headers.append(
            [
                language,
                stats_by_language[language]["vacancies_found"],
                stats_by_language[language]["vacancies_processed"],
                stats_by_language[language]["average_salary"],
            ]
        )
    table_instance = AsciiTable(headers, title)
    print(table_instance.table)