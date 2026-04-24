from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame

# register display
class RegisterDisplay(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        self.labels = []
        for i in range(3, -1, -1):
            label = QFrame(f"R{i}: 00000000")
            label.setFrameShape(QFrame.Shape.Box)
            label.setLineWidth(2)
            label.setStyleSheet("font-family: monospace; font-size: 13px; margin-bottom: 3px; background-color: #e7f6ff;")
            layout.addWidget(label)
            self.labels.append(label)

    def update_values(self, values):
        for i, val in enumerate(values[::-1]):
            #self.labels[i].setText(f"R{i}: {val:08b}") # enable to convert decimal -> binary
            self.labels[i].setStyleSheet("font-family: monospace; font-size: 13px; margin-bottom: 3px; background-color: #e7f6ff;")
            self.labels[i].setText(f"R{i}: {val}")
    