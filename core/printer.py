from terminaltables import AsciiTable


def print_statistics_table(stats_by_language, title):
    headers = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language, stats in stats_by_language.items():
        headers.append([
            language,
            stats["vacancies_found"],
            stats["vacancies_processed"],
            stats["average_salary"],
        ])
    table_instance = AsciiTable(headers, title)
    print(table_instance.table)