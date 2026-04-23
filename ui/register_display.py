from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

class RegisterDisplay(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        self.labels = []
        for i in range(4):
            label = QLabel(f"R{i}: 00000000")
            label.setStyleSheet("font-family: monospace; border: 0.25px solid gray; padding: 5px;")
            layout.addWidget(label)
            self.labels.append(label)

    def update_values(self, values):
        for i, val in enumerate(values):
            #self.labels[i].setText(f"R{i}: {val:08b}")
            self.labels[i].setText(f"R{i}: {val}")