from abc import abstractmethod, ABC
from base.data_models import SolverResponce
from base.data_models import TaskConfiguration, Curve
import numpy as np
from base.chebishev_dist import chebishev_roots
class BaseSolver(ABC):
    def __init__(self, config: TaskConfiguration):
        self.config = config

    def _to_curves(self, solve_result, x_grid):
        if "curves" in solve_result:
            return solve_result["curves"], solve_result.get("test_grid")

        # старый формат (интерполяция)
        if "interpolation" in solve_result:
            pred = np.asarray(solve_result["interpolation"])
            true = np.asarray(solve_result["true_values"])
            return [Curve("interpolation", x_grid, pred, true)], solve_result.get("test_grid")

        raise ValueError("unknown solve result format")

    def execute(self, step):
        start, end = self.config.bounds
        n = int(np.round((end - start) / step))
        temp_grid = (np.linspace(start, end, n + 1)
                     if self.config.dist == 'uniform'
                     else chebishev_roots(n, self.config.bounds))

        result = self.solve(temp_grid) if self.config.test_grid is None \
                       else self.solve(temp_grid, self.config.test_grid)


        if 'curves' in result:
            curves = result['curves']
            metrics = {c.name: self.calculate_metrics(c.y_pred, c.y_true) for c in curves}
            
            print('metrics:', {k: (type(v).__name__, v) for k, v in metrics.items()})
            return SolverResponce(
                test_grid=result.get('test_grid'),
                metrics=metrics,
                step=step,
                curves=curves,
            )

        # --- старый путь: интерполяция ---
        pred = np.asarray(result['interpolation'])
        true = np.asarray(result['true_values'])
        return SolverResponce(
            test_grid=result['test_grid'],
            true_values=true,
            interpolated=pred,
            metrics={'error': self.calculate_metrics(pred, true)},
            step=step,
        )
    
    @abstractmethod
    def solve(self, x_grid, test_grid = None):
        pass

    def calculate_metrics(self):
        pass