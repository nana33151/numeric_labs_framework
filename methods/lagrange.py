import numpy as np
from base.task_type import TaskType
from base.base_solver import BaseSolver
from base.data_models import TaskConfiguration

class LagrangeInterpolator(BaseSolver):
    def __init__(self, config:TaskConfiguration):
        super().__init__(config)

    def solve(self, x_grid, test_grid = None):
        f = self.config.f #f обязана быть векторизованой функцией
        print(x_grid)
        if test_grid is None:
            test_grid = (x_grid[:-1] + x_grid[1:])/2
        else:
            test_grid = test_grid
        print(test_grid)
        ans = []
        f_values = [f(y) for y in x_grid]
        for x in test_grid:
            values = []
            for x_i in x_grid:
                value = 1
                for x_j in x_grid:
                    if x_i != x_j:
                        value = value*(x-x_j)/(x_i-x_j)
                values.append(value)
            ans.append(np.array(f_values) @ np.array(values))

        return {'interpolation': ans,
                'true_values':np.array([f(y) for y in test_grid]),
                'test_grid': test_grid}

    def calculate_metrics(self, x, y):
        error  = np.max(np.abs(x - y))
        log_error = np.log10(error) if error > 1e-15 else np.nan

        return {'error': error,
                'log_error': log_error}

