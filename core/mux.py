class MUX:
    def __init__(self):
        # mux data input : register num
        self.mux = {
            0 : None,
            1 : 3,
            2 : 2,
            3 : 1
        }
        self.output = None
    
    def set_mux_output(self, data):
        self.mux_output = data
    
    def get_mux_mapping(self):
        return self.mux
    
    def get_linked_register(self, mux_input):
        return self.mux[mux_input]
    
    def get_mux_output(self):
        return self.mux_output



