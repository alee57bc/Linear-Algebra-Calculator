import pytest
from app.core.vector import Vector

def test_vector_dimension():
    vector = Vector([1, 2, 3])
    assert vector.dimension == 3

def test_vector_values():
    vector = Vector([1, 2, 3])
    assert vector[0] == 1
    assert vector[1] == 2
    assert vector[2] == 3

def test_vector_modification():
    vector = Vector([1, 2, 3])
    vector[0] = 5
    assert vector[0] == 5

def test_vector_rejects_empty_data():
    with pytest.raises(ValueError):
        Vector([])

def test_vector_rejects_non_list_data():
    with pytest.raises(TypeError):
        Vector("not a vector")

def test_vector_rejects_non_numeric_values():
    with pytest.raises(ValueError):
        Vector([1, 2, "hello"])

def test_vector_accepts_complex_values():
    v = Vector([
        1 + 2j,
        3 - 4j
    ])

    assert v[0] == 1 + 2j
    assert v[1] == 3 - 4j


def test_vector_copy_and_construction_do_not_alias_input():
    data = [1, 2]
    vector = Vector(data)
    copied = vector.copy()
    data[0] = 99
    copied[1] = 99
    assert vector.data == [1, 2]
    assert str(vector) == "[1.0 2.0]"
