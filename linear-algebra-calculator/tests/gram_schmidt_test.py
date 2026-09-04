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