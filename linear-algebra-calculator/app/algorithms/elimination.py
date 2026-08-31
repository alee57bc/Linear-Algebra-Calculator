from app.core.matrix import Matrix

def swap_rows(matrix, row1, row2):
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]

def scale_row(matrix, row, scalar):
    for column in range(matrix.columns):
        matrix[row][column] *= scalar

def add_multiple_of_row(matrix, source, target, scalar):
    for column in range(matrix.columns):
        matrix[target][column] += scalar * matrix[source][column]

def gaussian_elimination(matrix):
    result = matrix.copy()
    pivot_row = 0
    for pivot_column in range(result.columns):
        # Stop if we've processed every row
        if pivot_row >= result.rows:
            break

        # Find a row with a non-zero value in this column
        pivot = None
        for row in range(pivot_row, result.rows):
            if result[row][pivot_column] != 0:
                pivot = row
                break

        # No pivot in this column
        if pivot is None:
            continue

        # Move pivot row into position
        if pivot != pivot_row:
            swap_rows(result, pivot, pivot_row)

        # Eliminate values below the pivot
        for row in range(pivot_row + 1, result.rows):
            if result[row][pivot_column] != 0:
                scalar = (
                    result[row][pivot_column]
                    / result[pivot_row][pivot_column]
                )
                add_multiple_of_row(
                    result,
                    pivot_row,
                    row,
                    -scalar
                )
        pivot_row += 1
    return result

def rref(matrix):
    result = matrix.copy()
    pivot_row = 0
    for pivot_column in range(result.columns):
        if pivot_row >= result.rows:
            break

        # Find a non-zero pivot
        pivot = None
        for row in range(pivot_row, result.rows):
            if result[row][pivot_column] != 0:
                pivot = row
                break

        # No pivot in this column
        if pivot is None:
            continue

        # Move pivot row into position
        if pivot != pivot_row:
            swap_rows(result, pivot, pivot_row)

        # Normalize pivot to 1
        pivot_value = result[pivot_row][pivot_column]
        if pivot_value != 1:
            scale_row(result, pivot_row, 1 / pivot_value)

        # Eliminate above and below pivot
        for row in range(result.rows):
            if row != pivot_row:
                value = result[row][pivot_column]
                if value != 0:
                    add_multiple_of_row(
                        result,
                        pivot_row,
                        row,
                        -value
                    )
        pivot_row += 1
    return result

def rank(matrix):
    reduced = rref(matrix)
    count = 0

    for row in reduced.data:
        if any(value != 0 for value in row):
            count += 1
    return count