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


def predict_rub_salary_hh(vacancy):
    salary_data = vacancy.get("salary")
    if not salary_data:
        return None

    pay_from = salary_data.get("from")
    pay_to = salary_data.get("to")
    currency = salary_data.get("currency")

    if not is_rub_currency(currency):
        return None

    return compute_salary(pay_from, pay_to)


def predict_rub_salary_sj(vacancy):
    pay_from = vacancy.get("payment_from")
    pay_to = vacancy.get("payment_to")
    currency = vacancy.get("currency")

    if not currency or currency.lower() != "rub":
         return None

    if not pay_from and not pay_to:
        return None

    return compute_salary(pay_from, pay_to)