import base.router as router
from methods.lagrange import LagrangeInterpolator
import numpy as np
from base.task_type import TaskType
from base.base_solver import BaseSolver
from base.router import VisualisingRouter
from base.data_models import VisualiserConfiguration, TaskConfiguration

class Pipeline():
    def __init__(self, solver:BaseSolver, task_config: TaskConfiguration):
        self.solver = solver(task_config)
        self.task_config = task_config

    def run_pipeline(self):
        responces, steps = self.run()
        if self.task_config.task_type == TaskType.APPROX:
            log_errors = np.array([r.metrics['error'] for r in responces])
        else:
            log_errors = {
                name: np.array([r.metrics[name]['max_error'] for r in responces], dtype=float)
                for name in responces[0].metrics
            }
        best_responce = min(responces, key=lambda r: r.step)

        pointwise_errors = {
            name: [r.metrics[name]['errors'] for r in responces]
            for name in responces[0].metrics
        }

        config = VisualiserConfiguration(
            steps=steps,
            log_errors=log_errors,
            best_responce=best_responce,
            task_config=self.task_config
        )
        visualiser = VisualisingRouter[self.task_config.task_type]
        visualiser(config)

    def run(self):
        steps = self.task_config.step_grid
        responces = []
        for step in steps:
            solver_responce = self.solver.execute(step)
            responces.append(solver_responce)
        return [responces, steps]

