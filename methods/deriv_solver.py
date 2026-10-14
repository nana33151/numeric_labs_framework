# methods/deriv_solvers.py (или где у тебя солверы)
from methods.derivation import (
    BaseSchemaSolver,
    right_schema, central_schema,
    right_schema2f2, right_schema2f4,
    central_schema2f2, central_schema2f4,
)

DEFAULT_DERIV_SCHEMAS = [
    ('first_der_right',   right_schema,       1),
    ('first_der_centr',   central_schema,     1),
    ('second_der_right2', right_schema2f2,    2),
    ('second_der_right4', right_schema2f4,    2),
    ('second_der_centr2', central_schema2f2,  2),
    ('second_der_centr4', central_schema2f4,  2),
]

class DerivSolver(BaseSchemaSolver):
    def __init__(self, config):
        super().__init__(config, DEFAULT_DERIV_SCHEMAS)