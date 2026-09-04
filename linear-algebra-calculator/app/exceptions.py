class LinearAlgebraError(Exception):
    """Base exception for linear algebra errors."""

class DimensionMismatchError(LinearAlgebraError):
    def __init__(self, message="Dimensions are incompatible for this operation."):
        super().__init__(message)

class NonSquareMatrixError(LinearAlgebraError):
    def __init__(self, message="Operation requires a square matrix."):
        super().__init__(message)

class SingularMatrixError(LinearAlgebraError):
    def __init__(self, message="Matrix is singular and cannot be inverted."):
        super().__init__(message)

class LinearDependenceError(LinearAlgebraError):
    def __init__(self, message="Vectors must be linearly independent."):
        super().__init__(message)

class ZeroVectorError(LinearAlgebraError):
    def __init__(self, message="Operation cannot be performed with the zero vector."):
        super().__init__(message)