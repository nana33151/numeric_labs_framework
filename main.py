import numpy as np
from base.task_type import TaskType
from base.data_models import TaskConfiguration
from methods.lagrange import LagrangeInterpolator
from pipeline.pipeline import Pipeline
from methods.deriv_solver import DerivSolver

if __name__ == '__main__':
    """func = lambda y: (2+y**2+10*np.cos(y))/(10+y)
    bounds = [0.0, 10.0]
    l = bounds[1]-bounds[0]
    
    step_grid = np.array([5.0, 0.5, 0.2, 0.1, 0.08])
    temp_grid = np.linspace(bounds[0], bounds[1], 1000)
    task_config = TaskConfiguration(
        f=func,
        step_grid=step_grid,
        bounds=bounds,
        task_type=TaskType.APPROX,
        dist = 'chebishev',
        test_grid = temp_grid
    )

    pipeline = Pipeline(solver=LagrangeInterpolator, task_config=task_config)
    pipeline.run_pipeline()

    n_array = np.array([l//step for step in step_grid])

    task_config = TaskConfiguration(
            f=func,
            step_grid=step_grid,
            bounds=bounds,
            task_type=TaskType.APPROX,
            dist = 'uniform',
            test_grid = temp_grid
        )
    
    pipeline = Pipeline(solver=LagrangeInterpolator, task_config=task_config)
    pipeline.run_pipeline()"""
    
    func = lambda x: np.log(np.sin(x)**2 + 1)
    der1 = lambda x: 2*x*np.cos(x**2) / (np.sin(x**2) + 1)
    der2 = lambda x: 2*(np.cos(x**2) - 2*x**2) / (np.sin(x**2) + 1)

    bounds = [-1.5, 1.5]
    step_grid = np.array([0.5, 0.2, 0.1, 0.05])
    temp_grid = np.linspace(bounds[0], bounds[1], 1000)

    task_config = TaskConfiguration(
        f=func,
        step_grid=step_grid,
        bounds=bounds,
        task_type=TaskType.DERIV,
        dist='uniform',
        test_grid=temp_grid,
        first_analitical_der=der1,
        second_analitical_der=der2,
    )

    pipeline = Pipeline(solver=DerivSolver, task_config=task_config)
    pipeline.run_pipeline()