from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSpinBox


class SpinBox(QHBoxLayout):

    def __init__(self, label, min_val, max_val, default):
        super().__init__()
        self.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        self.addWidget(spin)