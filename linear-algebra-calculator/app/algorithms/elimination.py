from app.utils.numeric import is_zero, is_close

def swap_rows(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]

def scale_row(matrix, row, scalar):
    for column in range(matrix.columns):
        matrix[row][column] *= scalar

def add_multiple_of_row(matrix, source, target, scalar):
    for column in range(matrix.columns):
        matrix[target][column] += scalar * matrix[source][column]

def find_pivot_row(matrix, start_row, pivot_column):
    for row in range(start_row, matrix.rows):
        if not is_zero(matrix[row][pivot_column]):
            return row
    return None

def prepare_pivot(matrix, pivot_row, pivot_column):
    pivot = find_pivot_row(
        matrix,
        pivot_row,
        pivot_column
    )

    if pivot is None:
        return False

    if pivot != pivot_row:
        swap_rows(matrix, pivot, pivot_row)
    return True

def gaussian_elimination(matrix):
    result = matrix.copy()
    pivot_row = 0

    for pivot_column in range(result.columns):
        if pivot_row >= result.rows:
            break

        if not prepare_pivot(result, pivot_row, pivot_column):
            continue

        pivot_value = result[pivot_row][pivot_column]

        for row in range(pivot_row + 1, result.rows):
            value = result[row][pivot_column]
            if not is_zero(value):
                scalar = value / pivot_value
                add_multiple_of_row(result, pivot_row, row, -scalar)
        pivot_row += 1
    return result


def rref(matrix):
    result = matrix.copy()
    pivot_row = 0

    for pivot_column in range(result.columns):
        if pivot_row >= result.rows:
            break

        if not prepare_pivot(result, pivot_row, pivot_column):
            continue

        pivot_value = result[pivot_row][pivot_column]

        if not is_close(pivot_value, 1.0):
            scale_row(result, pivot_row, 1 / pivot_value)

        for row in range(result.rows):
            if row == pivot_row:
                continue

            value = result[row][pivot_column]

            if not is_zero(value):
                add_multiple_of_row(result, pivot_row, row, -value)
        pivot_row += 1
    return result

def rank(matrix):
    reduced = rref(matrix)
    count = 0

    for row in reduced.data:
        if any(not is_zero(value) for value in row):
            count += 1
    return count