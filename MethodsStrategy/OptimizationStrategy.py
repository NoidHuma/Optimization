from abc import abstractmethod, ABC


class OptimizationStrategy(ABC):

    def __init__(self, func_class):
        self._current_func = func_class

    def set_func(self, func_class):
        self._current_func = func_class

    def calculate_func(self, x, y):
        return self._current_func.calculate_func(x, y)

    @abstractmethod
    def optimize(self, initial_point, lr, max_iters, tolerance, **kwargs):
        pass
