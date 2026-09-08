from task_type import TaskType


ApproxVr = BaseVisualiser()

VisualisingRouter = {

    TaskType.APPROX: ApproxVR(),
    TaskType.SOLVING: SolveVR(),
    TaskType.CAUCHY: CauchyVR(),
    TaskType.BVP: BvpVR(),
    TaskType.PDE: PdeVR()

}