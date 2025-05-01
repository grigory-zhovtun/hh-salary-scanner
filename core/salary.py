from .extractors import extract_salary



def is_rub_currency(currency) -> bool:
    return bool(currency) and currency.lower() in ("rur", "rub")


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

    if not is_rub_currency(currency):
        return None

    return compute_salary(pay_from, pay_to)