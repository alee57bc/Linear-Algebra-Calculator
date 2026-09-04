import math
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.algorithms.inverse import inverse
from app.exceptions import NonSquareMatrixError
from app.utils.numeric import clean_number, is_zero
from app.exceptions import LinearDependenceError, SingularMatrixError

def eigenvalues(A: Matrix):
    if A.rows != A.columns:
        raise NonSquareMatrixError

    if A.rows != 2:
        raise NotImplementedError(
            "Eigenvalues are currently implemented only for 2x2 matrices."
        )

    a = A[0][0]
    b = A[0][1]
    c = A[1][0]
    d = A[1][1]
    trace = a + d
    det = a * d - b * c
    discriminant = trace ** 2 - 4 * det

    if discriminant < 0 and not is_zero(discriminant):
        raise ValueError("Matrix has complex eigenvalues.")

    if is_zero(discriminant):
        discriminant = 0.0

    sqrt_discriminant = math.sqrt(discriminant)
    lambda1 = (trace + sqrt_discriminant) / 2
    lambda2 = (trace - sqrt_discriminant) / 2
    return [clean_number(lambda1), clean_number(lambda2)]

def eigenvectors(A: Matrix):
    values = eigenvalues(A)
    vectors = []

    for eigenvalue in values:
        a = A[0][0] - eigenvalue
        b = A[0][1]
        c = A[1][0]
        d = A[1][1] - eigenvalue

        if not is_zero(b):
            vector = Vector([1.0, -a / b])
        elif not is_zero(c):
            vector = Vector([-d / c, 1.0])
        else:
            if is_zero(a):
                vector = Vector([1.0, 0.0])
            else:
                vector = Vector([0.0, 1.0])
        vectors.append(vector)
    return vectors

def diagonalize(A: Matrix):
    values = eigenvalues(A)
    vectors = eigenvectors(A)

    if len(vectors) != A.columns:
        raise LinearDependenceError

    P = Matrix([
        [vectors[column][row] for column in range(len(vectors))]
        for row in range(A.rows)])

    try:
        P_inverse = inverse(P)
    except SingularMatrixError:
        raise LinearDependenceError

    D = Matrix([
        [values[row] if row == column else 0.0
            for column in range(A.columns)]
        for row in range(A.rows)])

    return P, D, P_inverse
