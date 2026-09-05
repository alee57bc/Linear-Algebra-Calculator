from app.core.vector import Vector
from app.core.basic_vector_operations import vector_projection, norm
from app.utils.numeric import is_zero
from app.exceptions import LinearDependenceError
from app.results.calculation_step import CalculationStep

def gram_schmidt(vectors, record_steps=False):
    orthogonal = []
    steps = [] if record_steps else None

    for index, v in enumerate(vectors):
        u = Vector(v.data.copy())

        if steps is not None:
            steps.append(CalculationStep(description=f"Start with v{index + 1}", result=u.copy()))

        for basis_index, basis_vector in enumerate(orthogonal):
            proj = vector_projection(u, basis_vector)

            if steps is not None:
                steps.append(
                    CalculationStep(description=(f"Project v{index + 1} onto " f"u{basis_index + 1}"), result=proj.copy()))

            u = Vector([a - b for a, b in zip(u.data, proj.data)])

            if steps is not None:
                steps.append(CalculationStep(description=(f"Subtract projection from v{index + 1}"), result=u.copy()))

        if is_zero(norm(u)):
            raise LinearDependenceError

        orthogonal.append(u)

    if record_steps:
        return orthogonal, steps

    return orthogonal