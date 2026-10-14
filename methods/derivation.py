from base.base_solver import BaseSolver
import numpy as np
from base.data_models import Curve

def right_schema(f_array, step):
    right = (f_array[1:] - f_array[:-1])/step
    cut = slice(None, -1)  
    return right, cut

def central_schema(f_array, step):
    central = (f_array[2:] - f_array[:-2]) / (2 * step)
    cut = slice(1, -1)
    return central, cut

def right_schema2f2(f_array, step):
    right_second_f2 = (2*f_array[:-3] - 5*f_array[1:-2] + 4*f_array[2:-1] - f_array[3:])/(step**2)
    cut = slice(None, -3)  
    return right_second_f2, cut

def right_schema2f4(f_array, step):
    right_second_f4 = (45*f_array[:-5] - 154*f_array[1:-4] + 214*f_array[2:-3] - 156*f_array[3:-2] + 61*f_array[4:-1] - 10*f_array[5:]) / (12 * step**2)
    cut = slice(None, -5) 
    return right_second_f4, cut

def central_schema2f4(f_array, step):
    right_second_f4 = (-f_array[4:] + 16*f_array[3:-1] - 30*f_array[2:-2] + 16*f_array[1:-3] - f_array[:-4]) / (12 * step**2)
    cut = slice(2, -2) 
    return right_second_f4, cut

def central_schema2f2(f_array, step):
    central_second_f2 = (f_array[:-2]-2*f_array[1:-1] + f_array[2:])/(step**2)
    cut = slice(1,-1)
    return central_second_f2, cut

class BaseSchemaSolver(BaseSolver):
    def __init__(self, config, schema):
        super().__init__(config)
        self.schema = schema

    def solve(self, x_grid, test_grid = None):
        step = x_grid[1]-x_grid[0]
        f_array = np.array([self.config.f(x) for x in x_grid])

        curves = []
        for name,fn,order in self.schema:
            der, cut = fn(f_array, step)
            y = np.array([self.config.first_analitical_der(x) for x in x_grid[cut]] if order == 1 else 
                         [self.config.second_analitical_der(x) for x in x_grid[cut]])
            curves.append(Curve(name,x_grid[cut],der,y))

        return {'curves': curves,
                'test_grid': test_grid

        }
    
    def calculate_metrics(self, y_pred, y_true):
        y_pred = np.asarray(y_pred, dtype=float)
        y_true = np.asarray(y_true, dtype=float)
        errors = np.abs(y_pred - y_true)
        return {
            'errors': errors,            # поточечно — для графиков ошибки на оси x
            'max_error': float(errors.max()),
            'l2_error': float(np.sqrt(np.mean(errors**2))),
        }
