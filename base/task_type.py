from enum import Enum

class TaskType(Enum):
        APPROX = 'approximation'
        DERIV = 'derivation'
        SOLVING = 'solving'
        CAUCHY = 'cauchy'
        BVP = 'bvp'
        PDE = 'pde'

    