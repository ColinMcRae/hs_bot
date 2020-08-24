class TradeStation:
    def __init__(self, coords):
        self.name = 'Trade Station'
        self.coords = coords
        #planet statuses:
        #0 - not empty
        #1 - busy (for full unload)
        #2 - empty (when there are not cargos fot other destinations)
        self.status = 0
        #TODO scan cargo amount
        self.cargo = 0
