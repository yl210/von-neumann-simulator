import sys

from core.register import Register, ProgramCounter, InstructionRegister, initGPR
from core.ram import RAM
from core.mux import MUX
from core.demux import DEMUX
from core.decoder import Decoder
from core.alu import ALU
from core.cpu import run_cpu
from core.utils import *

# claude: modified from sample setup
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class CPUController(QObject):
    





    gpr = initGPR()
    pc = ProgramCounter(0)
    ir = InstructionRegister(0)
    ram = RAM()
    mux = MUX()
    dc = Decoder()
    demux = DEMUX()
    alu = ALU()


run_cpu(pc,ir, ram, dc, gpr, mux, demux, alu)
