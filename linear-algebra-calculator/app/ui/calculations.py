from dataclasses import dataclass, field
from app.core.matrix import Matrix
from app.core.vector import Vector
from app.core.basic_operations import add, subtract, scalar_multiply, multiply, transpose
from app.algorithms.elimination import gaussian_elimination, rref
from app.algorithms.determinant import determinant
from app.algorithms.inverse import inverse
from app.algorithms.gram_schmidt import gram_schmidt
from app.algorithms.decompositions import lu_decomposition, qr_decomposition
from app.algorithms.eigen import eigenvalues, eigenvectors, diagonalize

@dataclass
class CalculationResult:
    result: object
    steps: list = field(default_factory=list)
    extra_results: list = field(default_factory=list)

class CalculationController:
    def calculate(self, operation, matrix_a, matrix_b=None, scalar=None):
        if matrix_a is None:
            return

        if operation == "Addition":
            return CalculationResult(result=add(matrix_a, matrix_b))

        if operation == "Subtraction":
            return CalculationResult(result=subtract(matrix_a, matrix_b))

        if operation == "Scalar Multiplication":
            return CalculationResult(result=scalar_multiply(matrix_a, scalar))

        if operation == "Matrix Multiplication":
            return CalculationResult(result=multiply(matrix_a, matrix_b))

        if operation == "Transpose":
            return CalculationResult(result=transpose(matrix_a))

        if operation == "Gaussian Elimination":
            result, steps = gaussian_elimination(matrix_a, record_steps=True)
            return CalculationResult(result=result, steps=steps)

        if operation == "RREF":
            result, steps = rref(matrix_a, record_steps=True)
            return CalculationResult(result=result, steps=steps)

        if operation == "Determinant":
            result, steps = determinant(matrix_a, record_steps=True)
            return CalculationResult(result=result, steps=steps)

        if operation == "Inverse":
            result, steps = inverse(matrix_a, record_steps=True)
            return CalculationResult(result=result, steps=steps)

        if operation == "Gram-Schmidt":
            vectors = [
                Vector([
                    matrix_a[row][column]
                    for row in range(matrix_a.rows)])
                for column in range(matrix_a.columns)]

            result_vectors, steps = gram_schmidt(vectors, record_steps=True)

            result = Matrix([
                [result_vectors[column][row]
                    for column in range(len(result_vectors))]
                for row in range(matrix_a.rows)])

            return CalculationResult(result=result, steps=steps)

        if operation == "LU Decomposition":
            P, L, U, steps = lu_decomposition(matrix_a, record_steps=True)
            return CalculationResult(result=U, steps=steps, extra_results=[("P", P), ("L", L), ("U", U),])

        if operation == "QR Decomposition":
            Q, R, steps = qr_decomposition(matrix_a, record_steps=True)
            return CalculationResult(result=R, steps=steps, extra_results=[("Q", Q), ("R", R),])

        if operation == "Eigenvalues":
            values, steps = eigenvalues(matrix_a, record_steps=True)
            return CalculationResult(result=values, steps=steps)

        if operation == "Eigenvectors":
            vectors, steps = eigenvectors(matrix_a, record_steps=True)
            return CalculationResult(result=vectors, steps=steps)

        if operation == "Diagonalization":
            P, D, P_inverse, steps = diagonalize(matrix_a, record_steps=True)
            return CalculationResult(result=D, steps=steps, extra_results=[("P", P), ("D", D), ("P⁻¹", P_inverse),])

        raise ValueError(f"Unknown operation: {operation}")