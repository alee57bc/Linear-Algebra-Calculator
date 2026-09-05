from app.core.matrix import Matrix
from app.utils.numeric import format_number

def parse_matrix_text(text):
    lines = [line.strip()
        for line in text.strip().splitlines()
        if line.strip()]

    if not lines:
        raise ValueError("Clipboard does not contain matrix data.")

    data = []

    for line in lines:
        # Support commas or spaces
        values = line.replace(",", " ").split()

        row = [float(value) for value in values]

        data.append(row)

    column_count = len(data[0])

    if column_count == 0:
        raise ValueError("Matrix rows cannot be empty.")

    for row in data:
        if len(row) != column_count:
            raise ValueError("All pasted matrix rows must have the same number of values.")

    return Matrix(data)


def matrix_to_text(matrix: Matrix) -> str:
    return "\n".join(
        " ".join(format_number(value) for value in row)
        for row in matrix.data)