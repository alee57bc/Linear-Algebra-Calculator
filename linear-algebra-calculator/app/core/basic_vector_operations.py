import math
from app.core.vector import Vector
from app.utils.numeric import is_zero

def dot_product(u, v):
    if u.dimension != v.dimension:
        raise ValueError("Vectors must have the same dimension.")

    return sum(a * b for a, b in zip(u.data, v.data))

def cross_product(u, v):
    if u.dimension != 3 or v.dimension != 3:
        raise ValueError("Cross product requires 3D vectors.")

    return Vector([
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    ])

def norm(v):
    return math.sqrt(dot_product(v, v))

def vector_projection(u: Vector, v: Vector):
    if u.dimension != v.dimension:
        raise ValueError("Vectors must have the same dimension.")
    denominator = dot_product(v, v)

    if is_zero(denominator):
        raise ValueError("Cannot project onto the zero vector.")

    scalar = dot_product(u, v) / denominator

    return Vector([scalar * value for value in v.data])