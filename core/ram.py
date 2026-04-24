from core.utils import format_byte

class RAM:

    def __init__(self):
        self.ram = {
            0  : 0b00011110, 
            1  : 0b01000011,  
            2  : 0b01010001,  
            3  : 0b00101111,
            4  : 0b01000010,
            5  : 0b01010000,
            6  : 0b01110000,
            7  : 0x00,
            8  : 0b10011111,
            9  : 0b10000011,
            10 : 0b10011101, 
            11 : None,
            12 : None,
            13 : 0x00,
            14 : 0b00001001,
            15 : 0b00001100
        }          
    
    def __repr__(self):
        result = '{\n'
        for key in self.ram:
            result += (f'  {key} : {format_byte(self.ram[key])}\n')
        result += '}'
        return result

    def get_ram(self):
        return self.ram
    
    def read_from_ram(self, address):
        return self.ram[address]
    
    def write_to_ram(self, address, data):
        self.ram[address] = data