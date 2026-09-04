from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import transpose, multiply
from app.algorithms.gram_schmidt import gram_schmidt
from app.core.basic_vector_operations import norm
from app.utils.numeric import is_zero

def qr_decomposition(A: Matrix):
    columns = [
        Vector([A[row][col] for row in range(A.rows)])
        for col in range(A.columns)
    ]
    orthogonal = gram_schmidt(columns)
    orthonormal = []

    for vector in orthogonal:
        magnitude = norm(vector)
        if is_zero(magnitude):
            raise ValueError(
                "Matrix columns must be linearly independent."
            )
        orthonormal.append(
            Vector([value / magnitude
                for value in vector.data])
        )

    Q = Matrix([
        [orthonormal[col][row]
            for col in range(len(orthonormal))]
        for row in range(A.rows)
    ])

    R = multiply(transpose(Q), A)
    return Q, R