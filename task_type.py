from enum import Enum

class TaskType(Enum):
        APPROX = 'approximation'
        SOLVING = 'solving'
        CAUCHY = 'cauchy'
        BVP = 'bvp'
        PDE = 'pde'

    