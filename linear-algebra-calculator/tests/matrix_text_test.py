import pytest

from app.core.matrix import Matrix
from app.utils.matrix_text import parse_matrix_text, matrix_to_text


@pytest.mark.parametrize("text", ["1 2\n3 4", "1,2\n3,4", " \n1\t2\n\n3, 4\n"])
def test_parse_supported_separators(text):
    assert parse_matrix_text(text) == Matrix([[1, 2], [3, 4]])


@pytest.mark.parametrize("text, message", [
    (" \n", "Clipboard does not contain"),
    (",,,", "rows cannot be empty"),
    ("1 2\n3", "same number"),
    ("1 invalid", "could not convert"),
])
def test_parse_rejects_invalid_matrix(text, message):
    with pytest.raises(ValueError, match=message):
        parse_matrix_text(text)


def test_matrix_text_formats_values_and_round_trips():
    matrix = Matrix([[1, -2.5], [0, 3.25]])
    assert matrix_to_text(matrix) == "1 -2.5\n0 3.25"
    assert parse_matrix_text(matrix_to_text(matrix)) == matrix


def test_parse_scientific_notation():
    assert parse_matrix_text("1e2 -2.5e-1") == Matrix([[100, -0.25]])
