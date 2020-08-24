from game.config import WARP_PLANETS, HUBS

class CargoDelivery:
    def __init__(self, solarsystem):
        self.sol = solarsystem
        self.transports = solarsystem.transports
        self.planets = solarsystem.planets
        self.tradestations = solarsystem.tradestations

    def move_cargo_to_warp(self):

        while True:
            for transport in self.transports:
                if transport.status == 0:
                    #find dest
                    pass

                if transport.status == 1:
                    #check if docked
                    pass

                if transport.status == 2:
                    #if docked - load or unload
                    pass

                if transport.status == 3:
                    #send it to unload
                    pass

                if transport.status == 8:
                    # try to unload to hub
                    pass

                if transport.status == 9:
                    #find another planet to unload
                    pass
            break

    def sort_cargo(self):
        hub = self.__find_hub()
        print(hub)

    def __find_free_transport(self):
        for tr in self.transports:
            if tr.status == 0:
                return tr
        return None

    def __find_full_tradestation(self):
        for station in self.tradestations:
            if station.status == 0:
                return station

    def __find_full_external_planet(self):
        for planet in self.planets:
            if planet.status == 0:
                return planet

    def __find_hub(self):
        hubs = HUBS.keys()
        hub = None
        for planet in self.planets:
            if planet.name in hubs and planet.status == 0:
                hub = planet
                planet.status = 3
        return hub
