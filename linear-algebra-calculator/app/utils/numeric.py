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

def format_number(value: float, decimals: int = 2) -> str:
    value = clean_number(value)
    rounded = round(value, decimals)

    if rounded == int(rounded):
        return str(int(rounded))

    return f"{rounded:.{decimals}f}".rstrip("0").rstrip(".")

def clean_complex(value: complex):
    real = clean_number(value.real)
    imag = clean_number(value.imag)

    if is_zero(imag):
        return real

    return complex(real, imag)

def format_number(value, decimals: int = 2) -> str:
    if isinstance(value, complex):
        value = clean_complex(value)

        if not isinstance(value, complex):
            return format_number(value, decimals)

        real = round(value.real, decimals)
        imag = round(value.imag, decimals)

        if is_zero(real):
            if is_close(imag, 1.0):
                return "i"
            if is_close(imag, -1.0):
                return "-i"
            return f"{imag:g}i"

        sign = "+" if imag >= 0 else "-"

        imag_abs = abs(imag)

        if is_close(imag_abs, 1.0):
            imag_text = "i"
        else:
            imag_text = f"{imag_abs:g}i"

        return f"{real:g} {sign} {imag_text}"

    value = clean_number(value)
    rounded = round(value, decimals)

    if rounded == int(rounded):
        return str(int(rounded))

    return f"{rounded:.{decimals}f}".rstrip("0").rstrip(".")

def to_numeric(value):
    if isinstance(value, complex):
        return value

    return float(value)