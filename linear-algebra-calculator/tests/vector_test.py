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