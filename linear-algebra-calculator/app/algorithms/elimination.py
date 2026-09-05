from app.utils.numeric import is_zero, is_close
from app.results.calculation_step import CalculationStep
from app.utils.cleanup import clean_matrix

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

def record_step(steps, description, matrix):
    if steps is not None:
        steps.append(CalculationStep(description=description, result=matrix.copy()))

def prepare_pivot(matrix, pivot_row, pivot_column, steps=None):
    pivot = find_pivot_row(matrix, pivot_row, pivot_column)

    if pivot is None:
        return False

    if pivot != pivot_row:
        swap_rows(matrix, pivot, pivot_row)

        record_step(steps, f"R{pivot_row + 1} ↔ R{pivot + 1}", matrix)

    return True

def gaussian_elimination(matrix, record_steps=False):
    result = matrix.copy()
    steps = [] if record_steps else None
    pivot_row = 0

    for pivot_column in range(result.columns):
        if pivot_row >= result.rows:
            break

        if not prepare_pivot(result, pivot_row, pivot_column, steps):
            continue

        pivot_value = result[pivot_row][pivot_column]

        for row in range(pivot_row + 1, result.rows):
            value = result[row][pivot_column]
            if not is_zero(value):
                scalar = value / pivot_value
                add_multiple_of_row(result, pivot_row, row, -scalar)

                record_step(steps, (f"R{row + 1} ← R{row + 1} " f"+ ({-scalar})R{pivot_row + 1}"), result)
        pivot_row += 1

    if record_steps:
        return result, steps

    return result

def rref(matrix, record_steps=False):
    result = matrix.copy()
    steps = [] if record_steps else None
    pivot_row = 0

    for pivot_column in range(result.columns):
        if pivot_row >= result.rows:
            break

        if not prepare_pivot(result, pivot_row, pivot_column, steps):
            continue

        pivot_value = result[pivot_row][pivot_column]

        if not is_close(pivot_value, 1.0):
            scalar = 1 / pivot_value
            scale_row(result, pivot_row, scalar)

            record_step(steps, f"R{pivot_row + 1} ← ({scalar})R{pivot_row + 1}", result)

        for row in range(result.rows):
            if row == pivot_row:
                continue

            value = result[row][pivot_column]

            if not is_zero(value):
                add_multiple_of_row(result, pivot_row, row, -value)

                record_step(steps, (f"R{row + 1} ← R{row + 1} " f"+ ({-value})R{pivot_row + 1}"), result)

        pivot_row += 1

    if record_steps:
        return result, steps

    return result

def rank(matrix):
    reduced = rref(matrix)
    count = 0

    for row in reduced.data:
        if any(not is_zero(value) for value in row):
            count += 1
    return count