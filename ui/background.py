from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter

class Background(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.bg = QPixmap(image_path)

    # sets wire background
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg)