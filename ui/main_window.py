from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QPixmap
from core.cpu import *
from ui.alu_symbol import ALUSymbol
from ui.background import Background

class EmulatorGUI(QMainWindow):
    def __init__(self, pc, ir, ram, dc, gpr, mx, dx, alu):
        super().__init__()
        # Window size
        self.setFixedSize(1000, 780)
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

        # state machine
        self.state_types = ['Fetching', 'Decoding', 'Executing', 'Completed']
        self.state_counter = 0

        self.dc_output = None

        # --- MAIN LAYOUT ---
        central_widget = Background('C:/Users/yliao/Documents/GitHub/z18100-simulator/wire overlay.png')
        self.setCentralWidget(central_widget)

        main_v_layout = QVBoxLayout(central_widget)

        # 1. TOP SECTION: Registers (Horizontally across)
        main_v_layout.addSpacing(20)
        reg_h_layout = QHBoxLayout()
        self.reg_labels = []
        for i in range(4):
            lbl = QLabel(f"R{i}: 0")
            lbl.setStyleSheet("""
                font-family: 'Segoe UI', sans-serif; 
                font-size: 13px;
                border: 2px solid #444; 
                padding: 15px; 
                background: #ffffff;
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
        left_side_container.setSpacing(4)

        # mux
        self.mux_frame = QFrame()
        self.mux_frame.setFrameShape(QFrame.Shape.Box)
        self.mux_frame.setLineWidth(2)
        self.mux_frame.setFixedSize(400,80)
        self.mux_frame.setStyleSheet("background-color: #e7f6ff;")

        mux_v = QVBoxLayout(self.mux_frame)
        mux_v.setContentsMargins(5, 10, 5, 10)
        mux_v.setSpacing(20)

        mux_connect = QHBoxLayout()
        mux_connect.setSpacing(0)
        for i in range(4):
            label = QLabel(f"D{i}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-family: monospace; font-size: 13px;")
            mux_connect.addWidget(label)
        mux_v.addLayout(mux_connect)

        mux_label = QLabel('MUX')
        mux_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mux_label.setStyleSheet("font-family: monospace; font-size: 15px; font-weight: bold;")
        mux_v.addWidget(mux_label)

        mux_v.addStretch()
        left_side_container.addWidget(self.mux_frame)
        left_side_container.addSpacing(30)

        # demux
        self.demux_frame = QFrame()
        self.demux_frame.setFrameShape(QFrame.Shape.Box)
        self.demux_frame.setLineWidth(2)
        self.demux_frame.setFixedSize(400,80)
        self.demux_frame.setStyleSheet("background-color: #e7f6ff;")
        left_side_container.addWidget(self.demux_frame)

        demux_v = QVBoxLayout(self.demux_frame)
        demux_v.setContentsMargins(5, 10, 5, 10)
        demux_v.setSpacing(20)

        demux_connect = QHBoxLayout()
        demux_connect.setSpacing(0)
        for i in range(2):
            label = QLabel(f"F{i}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-family: monospace; font-size: 13px;")
            demux_connect.addWidget(label)
        demux_v.addLayout(demux_connect)

        demux_label = QLabel('DEMUX')
        demux_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        demux_label.setStyleSheet("font-family: monospace; font-size: 15px; font-weight: bold;")
        demux_v.addWidget(demux_label)

        demux_v.addStretch()
        left_side_container.addWidget(self.demux_frame)
        left_side_container.addSpacing(-10)

        self.alu_symbol = ALUSymbol()
        left_side_container.addWidget(self.alu_symbol)


        left_side_container.addStretch() # Push buttons to the bottom
        button_h_layout = QHBoxLayout()
        self.step_btn = QPushButton("MANUAL STEP")
        self.step_btn.setFixedSize(200, 60)
        self.auto_btn = QPushButton("AUTO RUN")
        self.auto_btn.setCheckable(True)
        self.auto_btn.setFixedSize(200,60)
        
        button_h_layout.addWidget(self.step_btn)
        button_h_layout.addWidget(self.auto_btn)
        
        left_side_container.addLayout(button_h_layout)
        bottom_h_layout.addLayout(left_side_container, stretch=1)
        
        # --- RIGHT SIDE: PC Display and RAM Table ---
        right_side_container = QVBoxLayout()
        
        # Program Counter Text (Reduced)
        self.pc_label = QLabel(f"Program Counter: {self.pc}")
        self.state_label = QLabel(f'Current State: {self.get_state()}')
        self.decode_label = QLabel(f'Decoder Selection: {self.dc.output}')
        self.pc_label.setStyleSheet("font-family: monospace; font-size: 12px; font-weight: bold; margin-bottom: 3px; color: #4292C6;")
        self.state_label.setStyleSheet("font-family: monospace; font-size: 12px; font-weight: bold; margin-bottom: 3px;")
        self.decode_label.setStyleSheet("font-family: monospace; font-size: 12px; font-weight: bold; margin-bottom: 3px;")
        self.state_label.setFixedWidth(210)
        self.decode_label.setFixedWidth(300)
        right_side_container.addWidget(self.pc_label)
        right_side_container.addWidget(self.state_label)
        right_side_container.addWidget(self.decode_label)

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
            '''
            print(f'ADDR:{self.pc.getCounter()}  OP: {bin(self.ir.opcode)}  OPE: {bin(self.ir.operand)}')
            print(f'gpr: {self.gpr}')
            print(f'demux: {self.dx.get_demux()}')
            print(f'ram: {repr(self.ram)}')
            print('\n')
            '''

        self.state_counter += 1
        self.refresh_ui()

    def get_state(self):
        state_idx = self.state_counter % 3
        return self.state_types[state_idx]
    
    def refresh_ui(self):
        # update labels
        self.pc_label.setText(f"Program Counter: {self.pc}")
        self.state_label.setText(f"Current State: {self.get_state()}")
        dc_text = self.dc_output[1] if self.dc_output != None else 'N/A'
        self.decode_label.setText(f"Current Activity: {dc_text}")

        # Update Registers
        for i in range(len(self.registers)):
            reg_idx = len(self.registers) - 1 - i
            self.reg_labels[i].setText(f"R{reg_idx}: {self.registers[reg_idx].read_reg()}")
            self.reg_labels[i].setStyleSheet("font-family: 'Segoe UI', sans-serif; font-size: 13px; border: 2px solid #444; padding: 15px; background: #e7f6ff;")

        self.mux_frame.setStyleSheet("background-color: #e7f6ff;")
        self.demux_frame.setStyleSheet("background-color: #e7f6ff;")
        self.alu_symbol.draw_alu_inputs(self.dx.get_data(0), self.dx.get_data(1))
        self.alu_symbol.setStyleSheet("font-family: monospace; font-size: 15px;")
        self.alu_symbol.update_alu_color('e7f6ff')

        if self.dc_output != None:
            current_selection = self.dc_output[0]
            #print(current_selection)
            if current_selection < 4:
                highlight_idx = len(self.registers) - 1 - current_selection
                self.reg_labels[highlight_idx].setStyleSheet("font-family: 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; border: 2px solid #444; padding: 15px; background: #8dcfec;")
            elif current_selection == 4:
                self.mux_frame.setStyleSheet("font-family: monospace; font-size: 15px; font-weight: bold; background: #8dcfec;")
            elif current_selection == 5:
                self.demux_frame.setStyleSheet("font-family: monospace; font-size: 15px; font-weight: bold; background: #8dcfec;")
            elif current_selection == 6 or current_selection == 7:
                self.alu_symbol.update_alu_color('8dcfec')
                self.alu_symbol.draw_alu_inputs(self.dx.get_data(0), self.dx.get_data(1))
                self.alu_symbol.setStyleSheet("font-family: monospace; font-size: 15px; font-weight: bold")

        # Update RAM
        for i in self.ram.get_ram():
            self.ram_table.setItem(i, 0, QTableWidgetItem(f"{i:04b}"))
            #self.ram_table.setItem(i, 0, QTableWidgetItem(f"{i}"))
            if self.ram.get_ram()[i] == None:
                content = 'XXXXXXXX'
            else:
                content = format(self.ram.get_ram()[i], '08b')
                #content = self.ram.get_ram()[i]
            self.ram_table.setItem(i, 1, QTableWidgetItem(str(content)))
            
        self.ram_table.selectRow(self.pc.getCounter())

