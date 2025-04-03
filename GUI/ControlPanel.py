from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox

from GUI.InputField import InputField
from GUI.SpinBox import SpinBox


class ControlPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.control_layout = QVBoxLayout(self)
        self.control_layout.setSpacing(10)

    def _update_control_panel(self, optimization_strategy):
        # Поля ввода параметров (без вертикальных отступов)
        self.control_layout.addLayout(InputField("Шаг обучения (lr):", 'lr', '1e-3'))
        self.control_layout.addLayout(InputField("Точность (tolerance):", 'tolerance', '1e-4'))
        self.control_layout.addLayout(InputField("Нач. точка X:", 'x0', '3.5'))
        self.control_layout.addLayout(InputField("Нач. точка Y:", 'y0', '2.0'))

        # Спинбоксы для числовых параметров
        self.control_layout.addLayout(SpinBox("Макс. итераций:", 1, 10000, 100))
        self.control_layout.addLayout(SpinBox("Интервал анимации (мс):", 10, 1000, 50))

        # Горизонтальный контейнер для кнопки и выбора метода
        hbox = QHBoxLayout()
        hbox.setSpacing(5)  # Небольшой отступ между кнопкой и комбобоксом
        hbox.setContentsMargins(0, 0, 0, 0)

        # Кнопка запуска оптимизации
        self.start_btn = QPushButton("Запустить оптимизацию")
        self.start_btn.clicked.connect(self.start_optimization)
        hbox.addWidget(self.start_btn)

        # Метка и комбобокс выбора метода оптимизации
        hbox.addWidget(QLabel("Метод:"))
        self.optimization_combo = QComboBox()
        self.optimization_combo.addItems(self.optimization_strategies.keys())
        self.optimization_combo.currentTextChanged.connect(self._on_optimization_method_changed)
        hbox.addWidget(self.optimization_combo)

        self.control_layout.addLayout(hbox)

        func_layout = QHBoxLayout()
        func_layout.addWidget(QLabel("Функция:"))
        self.func_combo = QComboBox()
        self.func_combo.addItems(self.functions.keys())
        self.func_combo.currentTextChanged.connect(self._on_func_changed)
        func_layout.addWidget(self.func_combo)

        self.control_layout.addLayout(func_layout)

        # Добавляем растягивающий элемент внизу, чтобы прижать все вверх
        self.control_layout.addStretch()
