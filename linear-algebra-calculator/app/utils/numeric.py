EPSILON = 1e-10

def is_zero(value: float) -> bool:
    return abs(value) < EPSILON

def is_close(a: float, b: float) -> bool:
    return abs(a - b) < EPSILON

def clean_number(value: float) -> float:
    if is_zero(value):
        return 0.0
    rounded = round(value)

    if is_close(value, rounded):
        return float(rounded)

    return value

def clean_row(row):
    return [clean_number(value) for value in row]
