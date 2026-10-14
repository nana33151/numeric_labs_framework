from dataclasses import dataclass
import numpy as np
from base.task_type import TaskType
from typing import Optional

@dataclass
class SolverResponce:
    test_grid: np.array
    metrics: dict
    step: float
    x_nodes: Optional[np.array] = None
    curves: Optional[np.array] = None
    true_values: Optional[np.ndarray] = None
    interpolated: Optional[np.ndarray] = None

@dataclass
class TaskConfiguration:
    f: callable
    step_grid: np.array
    bounds: np.array
    task_type: TaskType
    dist: str
    test_grid: np.array
    first_analitical_der: Optional[callable] = None
    second_analitical_der: Optional[callable] = None
    true_int: Optional[callable] = None

@dataclass
class VisualiserConfiguration:
    steps: list
    log_errors: np.array
    best_responce: float
    task_config: TaskConfiguration
    pointwise_errors: Optional[np.ndarray] = None

@dataclass
class Curve:
    name: str
    x: np.ndarray
    y_pred: np.ndarray
    y_true: np.ndarray