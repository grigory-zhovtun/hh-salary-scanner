from terminaltables import AsciiTable


def terminal_print(data, title):
    headers = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language in data:
        headers.append(
            [
                language,
                data[language]["vacancies_found"],
                data[language]["vacancies_processed"],
                data[language]["average_salary"],
            ]
        )
    table_instance = AsciiTable(headers, title)
    print(table_instance.table)