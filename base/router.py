from base.task_type import TaskType
from visualisers.visualisers import *

VisualisingRouter = {

    TaskType.APPROX: approximation_visualise,
    TaskType.DERIV: derivative_visualise,
    TaskType.SOLVING: solving,
    TaskType.CAUCHY: cauchy,
    TaskType.BVP: bvp,
    TaskType.PDE: pde

}