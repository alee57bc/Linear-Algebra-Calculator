from app.algorithms.elimination import swap_rows, add_multiple_of_row
from app.utils.numeric import is_zero, clean_number, format_number
from app.exceptions import NonSquareMatrixError
from app.results.calculation_step import CalculationStep
from app.algorithms.elimination import record_step

def determinant(matrix, record_steps=False):
    if matrix.rows != matrix.columns:
        raise NonSquareMatrixError
    steps = [] if record_steps else None
    result = matrix.copy()
    det = 1.0
    swap_count = 0

    for pivot_column in range(result.columns):
        # Find a non-zero pivot
        pivot = None
        for row in range(pivot_column, result.rows):
            if not is_zero(result[row][pivot_column]):
                pivot = row
                break

        # No pivot means determinant is zero
        if pivot is None:
            if record_steps:
                return 0.0, steps
            return 0.0

        # Swap rows if necessary
        if pivot != pivot_column:
            swap_rows(result, pivot, pivot_column)
            swap_count += 1

            record_step(steps, f"R{pivot_column + 1} ↔ R{pivot + 1}", result)

        pivot_value = result[pivot_column][pivot_column]

        # Eliminate values below pivot
        for row in range(pivot_column + 1, result.rows):
            if not is_zero(result[row][pivot_column]):
                scalar = result[row][pivot_column] / pivot_value
                add_multiple_of_row(result, pivot_column, row, -scalar)
                record_step(steps, f"R{row + 1} ← R{row + 1} + ({format_number(-scalar)})R{pivot_column + 1}", result)

    # Product of diagonal
    for i in range(result.rows):
        det *= result[i][i]

    # Each row swap changes the sign
    if swap_count % 2 == 1:
        det *= -1

    det = clean_number(det)
    if record_steps:
        return det, steps
    return det
