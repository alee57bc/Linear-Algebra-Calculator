from app.core.matrix import Matrix
from app.core.vector import Vector
from app.utils.numeric import clean_number, clean_complex

def clean_value(value):
    if isinstance(value, complex):
        return clean_complex(value)
    return clean_number(value)

def clean_matrix(matrix):
    return Matrix([
        [clean_value(matrix[row][column])
            for column in range(matrix.columns)]
        for row in range(matrix.rows)])

def clean_vector(vector):
    return Vector([
        clean_number(value)
        for value in vector.data])