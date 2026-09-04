from app.core.matrix import Matrix
from app.core.vector import Vector
from app.exceptions import DimensionMismatchError

def add(a, b):
    if a.rows != b.rows or a.columns != b.columns:
        raise DimensionMismatchError
    data = []
    for row in range(a.rows):
        row_data = []
        for column in range(a.columns):
            value = a[row][column] + b[row][column]
            row_data.append(value)
        data.append(row_data)
    return Matrix(data)

def subtract(a, b):
    if a.rows != b.rows or a.columns != b.columns:
        raise DimensionMismatchError
    data = []
    for row in range(a.rows):
        row_data = []
        for column in range(a.columns):
            value = a[row][column] - b[row][column]
            row_data.append(value)
        data.append(row_data)
    return Matrix(data)

def scalar_multiply(matrix, scalar):
    data = []
    for row in range(matrix.rows):
        row_data = []
        for column in range(matrix.columns):
            value = matrix[row][column] * scalar
            row_data.append(value)
        data.append(row_data)
    return Matrix(data)

def multiply(a, b):
    if a.columns != b.rows:
        raise DimensionMismatchError

    data = []
    for row in range(a.rows):
        row_data = []
        for column in range(b.columns):
            value = 0.0
            for k in range(a.columns):
                value += a[row][k] * b[k][column]
            row_data.append(value)
        data.append(row_data)
    return Matrix(data)

def transpose(matrix):
    data = []
    for column in range(matrix.columns):
        row_data = []
        for row in range(matrix.rows):
            row_data.append(matrix[row][column])
        data.append(row_data)
    return Matrix(data)

def matrix_vector_multiply(matrix, vector):
    if matrix.columns != vector.dimension:
        raise DimensionMismatchError

    data = []

    for row in range(matrix.rows):
        value = 0.0
        for column in range(matrix.columns):
            value += matrix[row][column] * vector[column]
        data.append(value)

    return Vector(data)