from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPainter, QPen, QPolygon, QFont, QColor
#from core.demux import DEMUX

class ALUSymbol(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 200)
        self.fill_color = tuple(bytes.fromhex('e7f6ff'))
        self.inA = None
        self.inB = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = 400 #self.width()
        h = self.height()

        # Pen for outline
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        painter.setBrush(QColor(*self.fill_color))

        # ALU body shape (slanted polygon)
        points = QPolygon([
            QPoint(int(w * 0.25), int(h * 0.15)),  # top-left
            QPoint(int(w * 0.4), int(h * 0.15)),
            QPoint(int(w * 0.5), int(h * 0.6)), 
            QPoint(int(w * 0.6), int(h * 0.15)),
            QPoint(int(w * 0.75), int(h * 0.15)),  # top-right
            QPoint(int(w * 0.60), int(h * 0.85)),  # bottom-right
            QPoint(int(w * 0.40), int(h * 0.85)),  # bottom-left
        ])
        painter.drawPolygon(points)

        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        font = QFont('Segoe UI', 10)
        painter.setFont(font)
        painter.drawText(int(w * 0.32), int(h * 0.35), f'{self.inA}')
        painter.drawText(int(w * 0.59), int(h * 0.35), f'{self.inB}')
        painter.drawText(int(w * 0.41), int(h * 0.8), 'ALU OUTPUT')

    def update_alu_color(self, color):
        self.fill_color = tuple(bytes.fromhex(color))
        self.update()
    
    def draw_alu_inputs(self, inA, inB):
        self.inA = inA
        self.inB = inB
        self.update()