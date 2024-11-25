from constants import null_values


def pars_null(value: str | None = None):
    print(value)
    if not value or value in null_values or value == "":
        return None
    return value
