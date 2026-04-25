'''
GRADING FEATURES
1. CPU cycle machine: core.cpu.py line 20
2. Branch instruction: Manual increment until instruction 11 to watch program jump
3. Inheritance w/ MVC: register.py + ui.main_window.py line 218
4. UX Experience: ui.main_window.py, line 231
'''
import sys

import core, ui
from core.alu import ALU
from core.cpu import initGPR
from core.decoder import Decoder
from core.demux import DEMUX
from core.mux import MUX
from core.ram import RAM
from core.register import Register, InstructionRegister, ProgramCounter
from core.utils import *

from ui.register_display import RegisterDisplay
from ui.main_window import EmulatorGUI

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy)
from PyQt6.QtCore import QTimer, Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QPen, QPolygon, QColor, QFont

def main():
    # create instances
    pc = ProgramCounter(0)
    alu = ALU()
    dc = Decoder()
    dx = DEMUX()
    mx = MUX()
    ram = RAM()
    gpr = initGPR()
    ir = InstructionRegister(0)

    # gui
    app = QApplication(sys.argv)
    gui = EmulatorGUI(pc, ir, ram, dc, gpr, mx, dx, alu)
    gui.show()
    app.exec()

main()