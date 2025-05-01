_EXTRACTORS = []


def register_extractor(predicate):
    def decorator(fn):
        _EXTRACTORS.append((predicate, fn))
        return fn
    return decorator


def extract_salary(vacancy):
    for predicate, fn in _EXTRACTORS:
        if predicate(vacancy):
            return fn(vacancy)
    return None, None, None


@register_extractor(lambda v: isinstance(v.get("salary"), dict))
def extract_from_hh(vacancy):
    s = vacancy["salary"]
    return s.get("from"), s.get("to"), s.get("currency")


@register_extractor(lambda v: "payment_from" in v)
def extract_from_sj(vacancy):
    return vacancy.get("payment_from"), vacancy.get("payment_to"), vacancy.get("currency")