from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt, QTimer
from core.cpu import *

class EmulatorGUI(QMainWindow):
    def __init__(self, pc, ir, ram, dc, gpr, mx, dx, alu):
        super().__init__()
        # Window size
        self.setFixedSize(1000, 720)
        self.setWindowTitle("Von Neumann Computer Architecture Simulator")

        # Initial State
        self.pc = pc
        self.registers = gpr
        self.ram = ram
        self.ir = ir
        self.dc = dc
        self.gpr = gpr
        self.mx = mx
        self.dx = dx
        self.alu = alu

        # state
        self.state_types = ['Fetching', 'Decoding', 'Executing', 'Completed']
        self.state_counter = 0

        # --- MAIN LAYOUT ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_v_layout = QVBoxLayout(central_widget)

        # 1. TOP SECTION: Registers (Horizontally across)
        reg_h_layout = QHBoxLayout()
        self.reg_labels = []
        for i in range(4):
            lbl = QLabel(f"R{i}: 0")
            lbl.setStyleSheet("""
                font-family: 'Segoe UI', sans-serif; 
                font-size: 16px;
                border: 2px solid #444; 
                padding: 15px; 
                background: #fdfdfd;
            """)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            reg_h_layout.addWidget(lbl)
            self.reg_labels.append(lbl)
        main_v_layout.addLayout(reg_h_layout)
        main_v_layout.addSpacing(100)

        # 2. BOTTOM SECTION: Content split split split
        bottom_h_layout = QHBoxLayout()
        main_v_layout.addLayout(bottom_h_layout)

        # --- LEFT SIDE: ALU Symbol and Buttons ---
        left_side_container = QVBoxLayout()
        '''
        # **NEW: LARGE ALU SYMBOL**
        self.alu_symbol = ALUSymbol()
        left_side_container.addWidget(self.alu_symbol)
        '''
        left_side_container.addStretch() # Push buttons to the bottom
        
        button_h_layout = QHBoxLayout()
        self.step_btn = QPushButton("MANUAL STEP")
        self.step_btn.setFixedHeight(60)
        self.auto_btn = QPushButton("AUTO RUN")
        self.auto_btn.setCheckable(True)
        self.auto_btn.setFixedHeight(60)
        
        button_h_layout.addWidget(self.step_btn)
        button_h_layout.addWidget(self.auto_btn)
        
        left_side_container.addLayout(button_h_layout)
        bottom_h_layout.addLayout(left_side_container, stretch=1)
        
        # --- RIGHT SIDE: PC Display and RAM Table ---
        right_side_container = QVBoxLayout()
        
        # Program Counter Text (Reduced)
        
        pc_state_container = QHBoxLayout()
        self.pc_label = QLabel(f"PC: {self.pc}")
        self.state_label = QLabel(f'Current State: {self.get_state()}')
        self.pc_label.setStyleSheet("font-family: monospace; font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        self.state_label.setStyleSheet("font-family: monospace; font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        self.state_label.setFixedWidth(210)
        #self.pc_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pc_state_container.addWidget(self.pc_label)
        pc_state_container.addWidget(self.state_label)
        right_side_container.addLayout(pc_state_container)

        # RAM Table
        self.ram_table = QTableWidget(16, 2)
        self.ram_table.setHorizontalHeaderLabels(["Address", "Data"])
        self.ram_table.setFixedWidth(320)
        self.ram_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ram_table.setStyleSheet("font-family: monospace;")
        right_side_container.addWidget(self.ram_table)
        
        bottom_h_layout.addLayout(right_side_container)
        
        # Connections
        self.step_btn.clicked.connect(self.manual_step)
        self.auto_btn.clicked.connect(self.toggle_auto)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.manual_step)
        
        self.refresh_ui()

    def toggle_auto(self):
        if self.auto_btn.isChecked():
            self.timer.start(400)
            self.auto_btn.setText("STOP")
        else:
            self.timer.stop()
            self.auto_btn.setText("AUTO RUN")

    def manual_step(self):
        state = self.get_state()
        if state == 'Fetching':
            try:
                fetch(self.pc, self.ir, self.ram)
            except ValueError:
                self.step_btn.setEnabled(False)
                self.auto_btn.setEnabled(False)
                self.state_counter = -1
                self.timer.stop()
                return
        elif state == 'Decoding':
            self.ir_data = self.ir.read_from_ir()
            op = self.ir.opcode
            self.dc_output = decode(self.dc.get_decoder(), op)
        elif state == 'Executing':
            execute(self.dc_output, self.ir_data, self.gpr, self.ram, self.mx, self.dx, self.ir, self.alu, self.pc)
            print(f'ADDR:{self.pc.getCounter()}  OP: {bin(self.ir.opcode)}  OPE: {bin(self.ir.operand)}')
            print(f'gpr: {self.gpr}')
            print(f'demux: {self.dx.get_demux()}')
            print(f'ram: {repr(self.ram)}')
            print('\n')

        self.state_counter += 1
        self.refresh_ui()

    def get_state(self):
        state_idx = self.state_counter % 3
        return self.state_types[state_idx]

    def refresh_ui(self):
        # Update PC Label
        self.pc_label.setText(f"PC: {self.pc}")
        self.state_label.setText(f"Current State: {self.get_state()}")
        
        # Update Registers
        for i in range(len(self.registers)):
            self.reg_labels[i].setText(f"R{i}: {self.registers[i].read_reg()}")
        
        # Update RAM
        for i in self.ram.get_ram():
            #self.ram_table.setItem(i, 0, QTableWidgetItem(f"{i:04b}"))
            self.ram_table.setItem(i, 0, QTableWidgetItem(f"{i}"))
            if self.ram.get_ram()[i] == None:
                content = 'XXXXXXXX'
            else:
                #content = format(self.ram.get_ram()[i], '08b')
                content = self.ram.get_ram()[i]
            self.ram_table.setItem(i, 1, QTableWidgetItem(str(content)))
        
        self.ram_table.selectRow(self.pc.getCounter())

