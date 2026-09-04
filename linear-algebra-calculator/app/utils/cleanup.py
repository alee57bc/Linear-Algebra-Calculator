from app.core.matrix import Matrix
from app.core.vector import Vector
from app.utils.numeric import clean_number

def clean_matrix(matrix: Matrix) -> Matrix:
    return Matrix([
        [clean_number(matrix[row][column])
            for column in range(matrix.columns)]
        for row in range(matrix.rows)
    ])

def clean_vector(vector: Vector) -> Vector:
    return Vector([
        clean_number(value)
        for value in vector.data])