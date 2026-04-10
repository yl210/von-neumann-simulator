from utils import format_byte

class ALU:
    def __init__(self):
        self.a = None
        self.b = None
        self.outputs = {
            '+' : None,
            '-' : None,
        }
        self.output_type = ''
    
    def has_valid_inputs(self, a, b):
        if a != None and b != None:
            self.a = a
            self.b = b
            return True
        return False
    
    def add(self):
        #print(f'a: {self.a}, b: {self.b}')
        if not ALU.has_valid_inputs:
            return None
        self.outputs['+'] = self.a + self.b
        return '+'
    
    def sub(self):
        #print(f'a: {self.a}, b: {self.b}')
        if not ALU.has_valid_inputs:
            return None
        self.outputs['-'] = self.a - self.b
        return '-'
    
    def is_negative(self):
        return self.outputs[self.output_type] < 0
     

     