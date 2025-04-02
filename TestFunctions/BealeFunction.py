import numpy as np


class BealeFunction:
    """
    Класс, представляющий функцию Била и её градиент.
    Функция Била - это тестовая функция для оптимизации, имеющая глобальный минимум в точке (3, 0.5).

    Attributes:
        None
    """

    @staticmethod
    def calculate_func(x, y):
        y3_clipped = np.clip(y ** 3, -1e5, 1e5)  # Защита от переполнения
        term1 = (1.5 - x + x * y) ** 2
        term2 = (2.25 - x + x * y ** 2) ** 2
        term3 = (2.625 - x + x * y3_clipped) ** 2
        return term1 + term2 + term3

    @staticmethod
    def calculate_gradient(x, y):
        df_dx = (
                2 * (1.5 - x + x * y) * (y - 1) +
                2 * (2.25 - x + x * y ** 2) * (y ** 2 - 1) +
                2 * (2.625 - x + x * y ** 3) * (y ** 3 - 1)
        )

        df_dy = (
                2 * (1.5 - x + x * y) * x +
                2 * (2.25 - x + x * y ** 2) * (2 * x * y) +
                2 * (2.625 - x + x * y ** 3) * (3 * x * y ** 2)
        )

        return np.array([df_dx, df_dy])