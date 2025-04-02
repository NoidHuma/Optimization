import numpy as np


class SimplexFunction1:
    """
    Класс, представляющий первую функцию для симплекс-метода.

    Attributes:
        None
    """

    @staticmethod
    def calculate_func(x, y):
        return 2 * x ** 2 + 3 * y ** 2 + 4 * x * y - 6 * x - 3 * y

    @staticmethod
    def calculate_gradient(x, y):
        return np.array([4*x + 4*y - 6, 4*x + 6*y - 3])