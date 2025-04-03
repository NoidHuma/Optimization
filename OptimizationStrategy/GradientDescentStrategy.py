import numpy as np

from OptimizationStrategy.OptimizationStrategy import OptimizationStrategy
from TestFunctions.BealeFunction import BealeFunction


class GradientDescentStrategy(OptimizationStrategy):
    def __init__(self):
        super().__init__(BealeFunction)

    def optimize(self, initial_point, lr, max_iters, tolerance, **kwargs):
        path = [initial_point.copy()]
        current_point = initial_point.copy()
        for _ in range(max_iters):
            gradient = self.calculate_gradient(*current_point)
            current_point -= lr * gradient
            path.append(current_point.copy())
            if np.linalg.norm(gradient) < tolerance:
                break
        return path

    def calculate_gradient(self, x, y):
        return self._current_func.calculate_gradient(x, y)