from app.utils.numeric import (
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