from PyQt5.QtWidgets import QLineEdit


class ScientificLineEdit(QLineEdit):
    def value(self):
        try:
            return float(self.text().replace(',', '.'))
        except:
            return 0.0