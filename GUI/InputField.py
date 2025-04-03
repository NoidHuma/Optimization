from PyQt5.QtWidgets import QHBoxLayout, QLabel

from GUI.ScientificLineEdit import ScientificLineEdit


class InputField(QHBoxLayout):

    def __init__(self, label, field, default):
        super().__init__()
        self.addWidget(QLabel(label))
        edit = ScientificLineEdit()
        edit.setText(default)
        setattr(self, f'{field}_edit', edit)
        self.addWidget(edit)