from game.config import WARP_PLANETS

class Planet:
    def __init__(self, planet):
        #{'name': 'Stur', 'coords': [710, 305]}
        self.name = planet['name']
        self.coords = planet['coords']
        #planet statuses:
        #0 - not empty
        #1 - busy (for full unload)
        #2 - empty (when there are not cargos fot other destinations)
        #3 - hub loading
        #8 - hub clear
        #9 - hub full
        self.status = 0
        #TODO scan cargo amount
        self.cargo = 0
        self.warp = self.name in WARP_PLANETS
