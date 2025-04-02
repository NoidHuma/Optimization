import matplotlib
import numpy as np
from PyQt5.QtCore import QThreadPool, QTimer, Qt
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel,
                             QSpinBox, QPushButton, QHBoxLayout, QDockWidget,
                             QListWidget, QListWidgetItem, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Локальные импорты
from GUI.ScientificLineEdit import ScientificLineEdit
from MethodsStrategy.GradientDescentStrategy import GradientDescentStrategy
from MethodsStrategy.SimplexStrategy import SimplexStrategy
from TestFunctions.BealeFunction import BealeFunction
from TestFunctions.SimplexFunction1 import SimplexFunction1
from Visualization.SurfaceVisualization import SurfaceVisualization
from WorkerCalculations.CalculationWorker import CalculationWorker

matplotlib.use('Qt5Agg')


class MainWindow(QMainWindow):
    """
    Главное окно приложения для визуализации методов оптимизации.
    Позволяет выбирать метод оптимизации, тип визуализации и параметры,
    а также отображает процесс оптимизации в 3D и историю точек.
    """

    def __init__(self):
        """
        Инициализация главного окна приложения.
        Создает стратегии оптимизации и визуализации, настраивает интерфейс.
        """
        super().__init__()

        # Инициализация стратегий
        self._init_strategies()

        # Инициализация функций
        self._update_functions()

        # Настройка UI
        self._setup_ui()

        # Настройка графика
        self._setup_plot()

        # Настройка параметров и таймеров
        self._setup_parameters()

    def _init_strategies(self):
        """Инициализация доступных стратегий оптимизации и визуализации."""
        self.optimization_strategies = {
            "Градиентный спуск": GradientDescentStrategy(),
            "Симплекс-метод": SimplexStrategy()
        }

        # Текущая стратегия по умолчанию
        self.optimization_strategy = GradientDescentStrategy()

        self.visualization_strategy = SurfaceVisualization()

    def _update_functions(self):
        """Инициализация доступных функций в зависимости от выбранной стратегии оптимизации."""
        if isinstance(self.optimization_strategy, GradientDescentStrategy):
            self.functions = {
                "Функция Била": BealeFunction()
            }
        elif isinstance(self.optimization_strategy, SimplexStrategy):
            self.functions = {
                "Тест": SimplexFunction1(),
                "Функция Била": BealeFunction()
            }
        # else:
        #     # На случай, если добавится новая стратегия
        #     self.functions = {
        #
        #     }

        # Текущая функция по умолчанию
        self.function = None


    def _setup_ui(self):
        """Настройка пользовательского интерфейса."""
        # Основные настройки окна
        self.setWindowTitle("3D Оптимизатор с историей точек")
        self.setGeometry(100, 100, 1600, 900)

        # Главный виджет и layout
        main_widget = QWidget()
        self.main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Настройка панели управления
        self._setup_control_panel()

        # Настройка док-панели с историей точек
        self._setup_history_dock()

        # Инициализация текущей стратегии
        self.optimization_strategy = self.optimization_strategies[
            self.optimization_combo.currentText()
        ]

    def _setup_control_panel(self):
        """Настройка панели управления с элементами ввода, прижатыми к верху."""
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Убираем промежутки между элементами и прижимаем к верху
        control_layout.setSpacing(10)  # Убираем вертикальные отступы между элементами

        self.main_layout.addWidget(control_panel, 1)

        # Поля ввода параметров (без вертикальных отступов)
        self._add_input_field(control_layout, "Шаг обучения (lr):", 'lr', '1e-3')
        self._add_input_field(control_layout, "Точность (tolerance):", 'tolerance', '1e-4')
        self._add_input_field(control_layout, "Нач. точка X:", 'x0', '3.5')
        self._add_input_field(control_layout, "Нач. точка Y:", 'y0', '2.0')

        # Спинбоксы для числовых параметров
        self.iter_spin = self._add_spinbox(control_layout, "Макс. итераций:", 1, 10000, 100)
        self.speed_spin = self._add_spinbox(control_layout, "Интервал анимации (мс):", 10, 1000, 50)

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

        control_layout.addLayout(hbox)

        func_layout = QHBoxLayout()
        func_layout.addWidget(QLabel("Функция:"))
        self.func_combo = QComboBox()
        self.func_combo.addItems(self.functions.keys())
        self.func_combo.currentTextChanged.connect(self._on_func_changed)
        func_layout.addWidget(self.func_combo)

        control_layout.addLayout(func_layout)


        # Добавляем растягивающий элемент внизу, чтобы прижать все вверх
        control_layout.addStretch()


    def _setup_history_dock(self):
        """Настройка док-панели для отображения истории оптимизации."""
        self.dock = QDockWidget("История оптимизации", self)
        self.points_list = QListWidget()
        self.points_list.itemClicked.connect(self.focus_on_point)
        self.dock.setWidget(self.points_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

    def _setup_plot(self):
        """Настройка области для отображения графиков."""
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        plot_layout.addWidget(self.canvas)
        plot_layout.addWidget(self.toolbar)

        self.main_layout.addWidget(plot_widget, 3)

        # Инициализация графика
        self.update_visualization()

    def _setup_parameters(self):
        """Настройка параметров приложения и таймеров."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)

        # Переменные для хранения данных оптимизации
        self.optimization_path = []
        self.z_values = []
        self.current_frame = 0

        # Элементы графика
        self.path_line = None
        self.last_point = None
        self.selected_marker = None

    def _add_input_field(self, layout, label, field, default):
        """
        Добавляет поле ввода с меткой в указанный layout.

        Args:
            layout: QLayout, в который добавляется поле
            label: Текст метки
            field: Имя атрибута для хранения поля ввода
            default: Значение по умолчанию
        """
        container = QHBoxLayout()
        container.addWidget(QLabel(label))
        edit = ScientificLineEdit()
        edit.setText(default)
        setattr(self, f'{field}_edit', edit)
        container.addWidget(edit)
        layout.addLayout(container)

    def _add_spinbox(self, layout, label, min_val, max_val, default):
        """Добавление спинбокса."""
        container = QHBoxLayout()
        container.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        container.addWidget(spin)
        layout.addLayout(container)
        return spin

    def _on_optimization_method_changed(self, method_name):
        """
        Обработчик изменения метода оптимизации.

        Args:
            method_name: Название выбранного метода
        """
        self.optimization_strategy = self.optimization_strategies[method_name]
        self._update_functions()
        self.func_combo.blockSignals(True)
        self.func_combo.clear()        # Очищаем комбобокс
        self.func_combo.addItems(self.functions.keys()) # Добавляем новые элементы из словаря функций
        self.func_combo.blockSignals(False)
        self.func_combo.currentTextChanged.connect(self._on_func_changed)
        self.update_visualization()

    def _on_func_changed(self, func_name):
        """
        Обработчик изменения целевой функции.

        Args:
            func_name: Название выбранной функции
        """
        self.function = self.functions[func_name]
        self.optimization_strategy.set_func(self.function)
        self.update_visualization()

    def update_visualization(self):
        """Обновляет график в соответствии с текущими настройками."""
        self.figure.clear()

        # Создаем соответствующие оси
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Генерация данных для графика
        x = np.linspace(-4, 4, 40)
        y = np.linspace(-4, 4, 40)
        x, y = np.meshgrid(x, y)
        z = self.optimization_strategy.calculate_func(x, y)

        # Применение выбранной стратегии визуализации
        self.visualization_strategy.plot(self.ax, x, y, z)
        self.ax.view_init(elev=35, azim=-45)
        self.ax.dist = 8.5


        self.canvas.draw()

    def get_params(self):
        """
        Собирает параметры оптимизации из полей ввода.

        Returns:
            dict: Словарь с параметрами оптимизации
        """
        return {
            'lr': self.lr_edit.value(),
            'tolerance': self.tolerance_edit.value(),
            'initial_point': np.array([
                float(self.x0_edit.text().replace(',', '.')),
                float(self.y0_edit.text().replace(',', '.'))
            ]),
            'max_iters': self.iter_spin.value()
        }

    def start_optimization(self):
        """Запускает процесс оптимизации в отдельном потоке."""
        self.start_btn.setEnabled(False)
        self.clear_plot()

        worker = CalculationWorker(self.get_params(), self.optimization_strategy)
        worker.signals.resultReady.connect(self._handle_optimization_results)
        worker.signals.finished.connect(lambda: self.start_btn.setEnabled(True))
        QThreadPool.globalInstance().start(worker)

    def _handle_optimization_results(self, path):
        """
        Обрабатывает результаты оптимизации.

        Args:
            path: Список точек пути оптимизации
        """
        self.optimization_path = path
        self.z_values = [self.optimization_strategy.calculate_func(p[0], p[1]) for p in path]
        self._update_points_list()
        self.current_frame = 0
        self.timer.start(self.speed_spin.value())

    def _update_points_list(self):
        """Обновляет список точек в док-панели истории."""
        self.points_list.clear()
        for i, (point, z) in enumerate(zip(self.optimization_path, self.z_values)):
            item = QListWidgetItem(
                f"Iter {i}: X={point[0]:.4f}, Y={point[1]:.4f}, Z={z:.2f}"
            )
            self.points_list.addItem(item)

    def focus_on_point(self, item):
        """
        Центрирует график на выбранной точке из истории.

        Args:
            item: Выбранный элемент списка точек
        """
        index = self.points_list.row(item)
        point = self.optimization_path[index]
        x, y = point
        z = self.z_values[index]

        if self.selected_marker:
            self.selected_marker.remove()

        self.selected_marker = self.ax.scatter(
            [x], [y], [z],
            color='gold',
            s=120,
            edgecolor='black',
            zorder=20
        )

        # Настройка угла обзора
        self.ax.dist = 6
        self.ax.elev = 30
        self.ax.azim = -45 + (x + y) * 10
        self.canvas.draw()

    def update_animation(self):
        """Обновляет анимацию процесса оптимизации."""
        if self.current_frame >= len(self.optimization_path):
            self.timer.stop()
            self._highlight_final_point()
            return

        # Получаем данные для текущего кадра
        x = [p[0] for p in self.optimization_path[:self.current_frame + 1]]
        y = [p[1] for p in self.optimization_path[:self.current_frame + 1]]
        z = self.z_values[:self.current_frame + 1]

        # Обновляем линию пути
        if self.path_line is None:
            self.path_line, = self.ax.plot(x, y, z, 'r-', linewidth=1.5)
        else:
            self.path_line.set_data(x, y)
            self.path_line.set_3d_properties(z)

        # Обновляем текущую точку
        self._update_current_point(x[-1], y[-1], z[-1])
        self.canvas.draw()
        self.current_frame += 1

    def _update_current_point(self, x, y, z):
        """
        Обновляет отображение текущей точки на графике.

        Args:
            x: X-координата точки
            y: Y-координата точки
            z: Z-координата точки
        """
        if self.last_point:
            self.last_point.remove()

        self.last_point = self.ax.scatter(
            [x], [y], [z],
            color='lime',
            s=60,
            edgecolor='black',
            zorder=10
        )

    def _highlight_final_point(self):
        """Подсвечивает конечную точку оптимизации."""
        final_point = self.optimization_path[-1]
        self.ax.scatter(
            [final_point[0]], [final_point[1]], [self.z_values[-1]],
            color='magenta',
            s=150,
            marker='*',
            edgecolor='black',
            zorder=15
        )
        self.canvas.draw()

    def clear_plot(self):
        """Очищает график от предыдущих элементов."""
        for artist in [self.path_line, self.last_point, self.selected_marker]:
            if artist:
                artist.remove()

        self.path_line = None
        self.last_point = None
        self.selected_marker = None


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())