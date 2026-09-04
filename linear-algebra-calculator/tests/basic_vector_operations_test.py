import pytest, math
from app.core.vector import Vector
from app.core.basic_vector_operations import dot_product, cross_product, norm, vector_projection

def test_dot_product():
    u = Vector([1, 2, 3])
    v = Vector([4, 5, 6])
    result = dot_product(u, v)

    assert result == pytest.approx(32.0)

def test_dot_product_negative_values():
    u = Vector([1, -2, 3])
    v = Vector([4, 5, -6])
    result = dot_product(u, v)
    expected = 4 - 10 - 18

    assert result == pytest.approx(expected)

def test_dot_product_orthogonal():
    u = Vector([1, 0])
    v = Vector([0, 1])

    assert dot_product(u, v) == pytest.approx(0.0)

def test_dot_product_four_dimensions():
    u = Vector([1, 2, 3, 4])
    v = Vector([5, 6, 7, 8])
    result = dot_product(u, v)

    assert result == pytest.approx(70.0)

def test_dot_product_mismatched_dimensions():
    u = Vector([1, 2])
    v = Vector([3, 4, 5])

    with pytest.raises(ValueError):
        dot_product(u, v)

def test_cross_product():
    u = Vector([1, 2, 3])
    v = Vector([4, 5, 6])
    result = cross_product(u, v)
    expected = [-3.0, 6.0, -3.0]

    assert result.data == pytest.approx(expected)

def test_cross_product_basis_vectors():
    i = Vector([1, 0, 0])
    j = Vector([0, 1, 0])
    result = cross_product(i, j)
    expected = [0.0, 0.0, 1.0]

    assert result.data == pytest.approx(expected)

def test_cross_product_reverse_basis_vectors():
    i = Vector([1, 0, 0])
    j = Vector([0, 1, 0])
    result = cross_product(j, i)
    expected = [0.0, 0.0, -1.0]

    assert result.data == pytest.approx(expected)

def test_cross_product_parallel_vectors():
    u = Vector([1, 2, 3])
    v = Vector([2, 4, 6])
    result = cross_product(u, v)
    expected = [0.0, 0.0, 0.0]

    assert result.data == pytest.approx(expected)

def test_cross_product_invalid_dimension():
    u = Vector([1, 2])
    v = Vector([3, 4])

    with pytest.raises(ValueError):
        cross_product(u, v)

def test_cross_product_mismatched_dimensions():
    u = Vector([1, 2, 3])
    v = Vector([4, 5])

    with pytest.raises(ValueError):
        cross_product(u, v)

def norm(v: Vector):
    return math.sqrt(
        sum(value ** 2 for value in v.data)
    )

def test_norm_3d():
    v = Vector([1, 2, 2])
    result = norm(v)

    assert result == pytest.approx(3.0)

def test_norm_zero_vector():
    v = Vector([0, 0, 0])
    result = norm(v)

    assert result == pytest.approx(0.0)

def test_norm_negative_values():
    v = Vector([-3, -4])
    result = norm(v)

    assert result == pytest.approx(5.0)

def test_norm_four_dimensions():
    v = Vector([1, 2, 2, 4])
    result = norm(v)

    assert result == pytest.approx(5.0)

def test_projection():
    u = Vector([3, 4])
    v = Vector([1, 0])
    result = vector_projection(u, v)
    expected = [3.0, 0.0]

    assert result.data == pytest.approx(expected)

def test_projection_non_axis_aligned():
    u = Vector([3, 4])
    v = Vector([2, 2])
    result = vector_projection(u, v)
    expected = [3.5, 3.5]

    assert result.data == pytest.approx(expected)

def test_projection_orthogonal():
    u = Vector([1, 0])
    v = Vector([0, 1])
    result = vector_projection(u, v)
    expected = [0.0, 0.0]

    assert result.data == pytest.approx(expected)

def test_projection_onto_itself():
    v = Vector([3, 4])
    result = vector_projection(v, v)
    expected = [3.0, 4.0]

    assert result.data == pytest.approx(expected)

def test_projection_mismatched_dimensions():
    u = Vector([1, 2])
    v = Vector([3, 4, 5])

    with pytest.raises(ValueError):
        vector_projection(u, v)

def test_projection_zero_vector():
    u = Vector([1, 2])
    v = Vector([0, 0])

    with pytest.raises(ValueError):
        vector_projection(u, v)