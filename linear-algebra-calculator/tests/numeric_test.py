import pytest

from app.core.matrix import Matrix
from app.core.vector import Vector
from app.utils.cleanup import clean_matrix, clean_vector
from app.utils.numeric import (
    EPSILON,
    clean_complex,
    clean_row,
    format_number,
    is_zero,
    is_close,
    clean_number,
)

def test_is_zero():
    assert is_zero(1e-12)
    assert not is_zero(1e-4)

def test_is_close():
    assert is_close(1.0, 1.00000000001)
    assert not is_close(1.0, 1.1)

def test_clean_small_number():
    assert clean_number(-2.2e-16) == 0.0

def test_clean_near_integer():
    assert clean_number(2.9999999999999996) == 3.0


@pytest.mark.parametrize("value, expected", [
    (0, "0"), (1.234, "1.23"), (-2.5, "-2.5"),
    (1e-12, "0"), (1j, "i"), (-1j, "-i"), (2.5j, "2.5i"),
    (2 + 1j, "2 + i"), (2 - 1j, "2 - i"),
    (2 + 3j, "2 + 3i"), (2 - 3j, "2 - 3i"),
    (2 + 1e-12j, "2"),
])
def test_format_number(value, expected):
    assert format_number(value) == expected


def test_numeric_precision_and_boundaries():
    assert format_number(1.23456, decimals=4) == "1.2346"
    assert not is_zero(EPSILON)
    assert is_zero(EPSILON / 2)
    assert not is_close(0, EPSILON)
    assert clean_row([1e-12, 2.000000000001, 1.25]) == [0, 2, 1.25]
    assert clean_complex(1e-12 + 2.000000000001j) == 2j


def test_cleanup_returns_independent_values():
    matrix = Matrix([[1e-12, 2 + 1e-12j]])
    vector = Vector([1e-12, 1.25])
    cleaned_matrix, cleaned_vector = clean_matrix(matrix), clean_vector(vector)
    assert cleaned_matrix == Matrix([[0, 2]])
    assert cleaned_vector.data == [0, 1.25]
    cleaned_matrix[0][0] = 9
    cleaned_vector[0] = 9
    assert matrix[0][0] == 1e-12
    assert vector[0] == 1e-12
