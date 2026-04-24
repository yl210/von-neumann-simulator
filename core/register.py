from core.utils import format_byte

# inheritance
class Register:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'{format_byte(self.data)}'

    def read_reg(self):
        return self.data

    def write_to_reg(self, data_in):
        self.data = data_in

    def __add__(self, other):
        return self.data + other.data
    
    def __sub__(self, other):
        return self.data - other.data

class ProgramCounter(Register):
    def __init__(self, offset):
        self.counter = offset
    
    def __repr__(self):
        return f'{format_byte(self.counter)}'

    def increment_counter(self):
        self.counter += 1

    def getCounter(self):
        return self.counter
    
    def set_counter(self, offset):
        self.counter = offset

class InstructionRegister(Register):
    def __init__(self, data):
        super().__init__(data)
        self.opcode = InstructionRegister.set_opcode(self, data)
        self.operand = InstructionRegister.set_operand(self, data)

    def set_opcode(self, data):
        self.opcode = data >> 4

    def set_operand(self, data):
        self.operand = data & 0x0f

    def load_new_instruction(self, data):
        self.data = data

    def read_from_ir(self):
        return self.data
    