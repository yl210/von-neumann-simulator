class Decoder:
    def __init__(self):
        self.op = None
        self.output = None
        # codes which selections correspond to which action for execution
        self.decoder = {
            0 : 'Writing to Register 0',
            1 : 'Writing to Register 1',
            2 : 'Writing to Register 2',
            3 : 'Writing to Register 3',
            4 : 'Storing to Multiplexer',
            5 : 'Storing to De-multiplexer',
            6 : 'Adding numbers in ALU',
            7 : 'Subtracting numbers in ALU',
            8 : 'Testing if result is negative',
            9 : 'Writing result to RAM',
        }
    
    def get_decoder(self):
        return self.decoder

    def get_output(self):
        return self.output
    
    def get_active_selection(self):
        return self.decoder.get(self.op) if self.op != None else None



    