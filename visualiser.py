from abc import ABC, abstractmethod

class BaseVisualiser:
    def __init__(self):
        pass

    @abstractmethod
    def plot(self):
        pass

    def draw_table(self, table_data):
        pass