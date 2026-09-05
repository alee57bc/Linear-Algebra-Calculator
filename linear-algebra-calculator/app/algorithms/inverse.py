from app.algorithms.elimination import rref
from app.core.matrix import Matrix
from app.utils.numeric import is_close
from app.exceptions import NonSquareMatrixError, SingularMatrixError
from app.utils.cleanup import clean_matrix

def inverse(matrix, record_steps=False):
    if matrix.rows != matrix.columns:
        raise NonSquareMatrixError
    n = matrix.rows

    # Create augmented matrix [A | I]
    augmented_data = []

    for i in range(n):
        row = matrix[i][:]
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        augmented_data.append(row)
    augmented = Matrix(augmented_data)

    # Reduce [A | I] to [I | A^-1]
    if record_steps:
        reduced, steps = rref(augmented, record_steps=True)
    else:
        reduced = rref(augmented)
        steps = None

    # Verify left side is the identity matrix
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i == j else 0.0
            if not is_close(reduced[i][j], expected):
                raise SingularMatrixError

    # Extract right half
    inverse_data = []

    for i in range(n):
        inverse_data.append(
            reduced[i][n:])

    result = clean_matrix(Matrix(inverse_data))

    if record_steps:
        return result, steps

    return result