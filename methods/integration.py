import numpy as np
from base.task_type import TaskType
from base.base_solver import BaseSolver
from base.data_models import TaskConfiguration
from base.data_models import Curve


def trapezoid_schema(f_array, step):
    return (f_array[:-1] + f_array[1:]).sum()/2*step, slice(None, -1)

class Integrator(BaseSolver):
    def __init__(self, config, schema):
        super().__init__(config)
        self.schema = schema

    def solve(self, x_grid, test_grid = None):
        step = x_grid[1]-x_grid[0]
        f_array = np.array([self.config.f(x) for x in x_grid])
        curves = []
        for name, method in self.schema:
            output,cut = method(f_array, step)
            curves.append(Curve(name,np.array([step]),np.array([output]), np.array([self.config.true_int])))
            
        return {'curves': curves,
                            'test_grid': test_grid}
    
    def calculate_metrics(self, y_pred, y_true):
        return {'error': float(np.max(np.abs(y_pred - y_true)))}