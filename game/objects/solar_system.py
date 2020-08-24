import _pickle as pickle
class SolarSystem:
    def __init__(self, interface):
        # self.interface = interface
        # self.objects = interface.init_objects()
        # self.planets = interface.get_planets(self.objects['planet'])
        # self.tradestations = self.objects['tradestation']

        #STUB
        with open('sol_objects.pkl', 'rb') as file:
            self.objects = pickle.load(file)
        with open('sol_tradestations.pkl', 'rb') as file:
            self.tradestations = pickle.load(file)
        with open('sol_planets.pkl', 'rb') as file:
            self.planets = pickle.load(file)

    def debug(self):
        print(self.objects)
