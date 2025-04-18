def predict_rub_salary(vacancy):
    if isinstance(vacancy.get("salary"), dict):
        pay_from = vacancy["salary"].get("from")
        pay_to = vacancy["salary"].get("to")
        currency = vacancy["salary"].get("currency")
    else:
        pay_from = vacancy.get("payment_from")
        pay_to = vacancy.get("payment_to")
        currency = vacancy.get("currency")

    pay_from = None if not pay_from else pay_from
    pay_to = None if not pay_to else pay_to
    if not currency or currency.lower() not in ("rur", "rub"):
        return None

    if pay_from is not None and pay_to is not None:
        return (pay_from + pay_to) / 2
    if pay_from is not None:
        return pay_from * 1.2
    if pay_to is not None:
        return pay_to * 0.8
    return None