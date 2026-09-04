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