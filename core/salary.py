from .extractors import extract_salary



def is_rub_currency(currency) -> bool:
    return bool(currency) and currency.lower() in ("rur", "rub")


def normalize_pay(value):
    return None if not value else value


def compute_salary(pay_from, pay_to):
    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    if pay_from:
        return pay_from * 1.2
    if pay_to:
        return pay_to * 0.8
    return None


def predict_rub_salary(vacancy):
    pay_from, pay_to, currency = extract_salary(vacancy)

    pay_from = normalize_pay(pay_from)
    pay_to   = normalize_pay(pay_to)

    if not is_rub_currency(currency):
        return None

    return compute_salary(pay_from, pay_to)