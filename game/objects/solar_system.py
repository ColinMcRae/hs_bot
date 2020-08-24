class SolarSystem:
    def __init__(self, interface):
        self.interface = interface
        self.objects = interface.init_objects()
        self.planets = interface.get_planets(self.objects['planet'])
        self.tradestations = self.objects['tradestation']

    def debug(self):
        print(self.objects)
