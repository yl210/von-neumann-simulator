class DEMUX:
    def __init__(self):
        self.demux = {
            0 : None,
            1 : None
        }

    def store_demux_input(self, location, data):
        self.demux[location] = data
    
    def get_demux(self):
        return self.demux
    
    def get_data(self, index):
        return self.demux[index]


