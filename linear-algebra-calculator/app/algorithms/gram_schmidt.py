from app.core.vector import Vector
from app.core.basic_vector_operations import vector_projection, norm
from app.utils.numeric import is_zero

def gram_schmidt(vectors: list[Vector]):
    orthogonal = []

    for v in vectors:
        u = Vector(v.data.copy())
        for basis_vector in orthogonal:
            proj = vector_projection(u, basis_vector)
            u = Vector([
                a - b
                for a, b in zip(u.data, proj.data)
            ])

        if is_zero(norm(u)):
            raise ValueError(
                "Vectors must be linearly independent."
            )
        orthogonal.append(u)
    return orthogonal