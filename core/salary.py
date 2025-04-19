def extract_salary_from_dict(vacancy):
    salary = vacancy["salary"]
    return salary.get("from"), salary.get("to"), salary.get("currency")


def extract_salary_from_fields(vacancy):
    return vacancy.get("payment_from"), vacancy.get("payment_to"), vacancy.get("currency")


def is_rub_currency(currency) -> bool:
    return bool(currency) and currency.lower() in ("rur", "rub")


def normalize_pay(value):
    return None if not value else value


def compute_salary(pay_from, pay_to):
    if pay_from is not None and pay_to is not None:
        return (pay_from + pay_to) / 2
    if pay_from is not None:
        return pay_from * 1.2
    if pay_to is not None:
        return pay_to * 0.8
    return None


def predict_rub_salary(vacancy):
    extractor = (
        extract_salary_from_dict
        if isinstance(vacancy.get("salary"), dict)
        else extract_salary_from_fields
    )
    pay_from, pay_to, currency = extractor(vacancy)

    pay_from = normalize_pay(pay_from)
    pay_to   = normalize_pay(pay_to)

    if not is_rub_currency(currency):
        return None

    return compute_salary(pay_from, pay_to)