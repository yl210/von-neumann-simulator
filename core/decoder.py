class Decoder:
    def __init__(self):
        self.op = None
        self.output = None
        self.decoder = {
            0 : 'gpr_0',
            1 : 'gpr_1',
            2 : 'gpr_2',
            3 : 'gpr_3',
            4 : 'mux',
            5 : 'demux',
            6 : 'alu_add',
            7 : 'alu_minus',
            8 : 'and_a',
            9 : 'ram_we',
        }
    
    def get_decoder(self):
        return self.decoder



    