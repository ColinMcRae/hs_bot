# from game.objects import Transport, Planet
from game.objects.trade_station import TradeStation
from game.objects.planet import Planet
from game.objects.transport import Transport

class SolarSystem:
    def __init__(self, interface):
        self.interface = interface
        self.objects = interface.init_objects()
        # self.planets = []
        # self.tradestations = []
        # self.transports = []
        self.__init_planets()
        self.__init_transports()
        self.__init_tradestations()

    def debug(self):
        print(self.objects)

    def __init_transports(self):
        self.transports = []
        for tr in self.objects['transportcontrol']:
            self.transports.append(Transport(tr, self.interface))

    def __init_planets(self):
        self.planets = []
        screen_planets = self.interface.get_planets(self.objects['planet'])
        for planet in screen_planets:
            self.planets.append(Planet(planet))

    def __init_tradestations(self):
        self.tradestations = []
        for ts in self.objects['tradestation']:
            self.tradestations.append(TradeStation(ts))
