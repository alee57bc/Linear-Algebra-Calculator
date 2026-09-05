from app.core.vector import Vector
from app.algorithms.gram_schmidt import gram_schmidt
from app.core.basic_vector_operations import dot_product

def test_gram_schmidt_two_vectors():
    vectors = [
        Vector([1, 1]),
        Vector([1, 0])
    ]
    result = gram_schmidt(vectors)

    assert len(result) == 2
    assert abs(dot_product(result[0], result[1])) < 1e-10

def test_gram_schmidt_records_steps():
    vectors = [
        Vector([1, 1]),
        Vector([1, 0])
    ]
    result, steps = gram_schmidt(
        vectors,
        record_steps=True
    )

    assert len(result) == 2
    assert len(steps) > 0
    assert steps[0].description
    assert isinstance(steps[0].result, Vector)

def test_gram_schmidt_without_steps_returns_vectors():
    vectors = [
        Vector([1, 1]),
        Vector([1, 0])
    ]
    result = gram_schmidt(vectors)

    assert isinstance(result, list)
    assert len(result) == 2