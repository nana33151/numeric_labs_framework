from abc import ABC, abstractmethod

class BaseSolver:
    def __init__(self):
        pass

    @abstractmethod
    def solve(self):
        pass

    def calculate_metrics(self):
        pass