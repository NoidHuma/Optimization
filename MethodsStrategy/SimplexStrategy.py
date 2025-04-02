import numpy as np

from MethodsStrategy.OptimizationStrategy import OptimizationStrategy
from TestFunctions.SimplexFunction1 import SimplexFunction1


class SimplexStrategy(OptimizationStrategy):
    def __init__(self):
        super().__init__(SimplexFunction1)

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