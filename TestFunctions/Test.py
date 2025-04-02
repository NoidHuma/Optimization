import numpy as np


class Test:
    """
    Класс, представляющий функцию Била и её градиент.
    Функция Била - это тестовая функция для оптимизации, имеющая глобальный минимум в точке (3, 0.5).

    Attributes:
        None
    """

    @staticmethod
    def calculate_func(x, y):
        return x + y

    @staticmethod
    def calculate_gradient(x, y):
        return np.array([1, 1])