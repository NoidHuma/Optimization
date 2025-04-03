from abc import ABC, abstractmethod


class VisualizationStrategy(ABC):
    @abstractmethod
    def plot(self, ax, x, y, z):
        pass