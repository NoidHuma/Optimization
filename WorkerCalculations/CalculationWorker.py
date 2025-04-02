from PyQt5.QtCore import QRunnable

from WorkerCalculations.WorkerSignals import WorkerSignals


class CalculationWorker(QRunnable):
    def __init__(self, params, strategy):
        super().__init__()
        self.signals = WorkerSignals()
        self.params = params
        self.strategy = strategy

    def run(self):
        path = self.strategy.optimize(
            initial_point=self.params['initial_point'],
            lr=self.params['lr'],
            max_iters=self.params['max_iters'],
            tolerance=self.params['tolerance']
        )
        self.signals.resultReady.emit(path)
        self.signals.finished.emit()
