# issue here
def format_byte(input):
    if isinstance(input, bytearray):
        return (f'0x{input[0]:02x}')
    elif isinstance(input, int):
        return (f'0x{input:04b}')

def get_lsb(n):
    return (n & 0x0001)