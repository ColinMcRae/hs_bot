from controller import clicker
from game.config import HUBS

class Transport:
    """
    statuses
    # 0 - idle
    # 1 - flying
    # 2 - doxked
    # 3 - loaded
    # 4 - completed
    # 8 - unloading to hub
    # 9 - unloading
    """
    def __init__(self, button, control_interface):
        self.button = button
        self.control = control_interface
        self.status = 0
        self.destination = None
        self.visited = []
        self.hub = None
        self.full = False
        self.load = 0
        self.capacity = 24

    def reset_task(self):
        self.status = 0
        self.destination = ''
        self.visited = []
        self.hub = ''
        self.full = False
        print(self.__hash__(), 'reset')

    def send_to_dest(self, dest):
        self.status = 1
        self.destination = dest
        clicker.leftclick(self.button)
        clicker.rightclick(dest.coords)

        #DEBUG
        print(self.__hash__(), 'sending to', dest.name)

    def send_to_hub(self):
        self.destination = self.hub
        self.status = 8
        clicker.leftclick(self.button)
        clicker.rightclick(self.hub.coords)

    def unload(self):
        self.load = 0

        # DEBUG
        print(self.__hash__(), 'unloading at', self.destination.name)

        #control.unload

    def load_all(self):
        self.status = 3
        # control.load
        # self.load = self.control.transport_load()

        # DEBUG
        print(self.__hash__(), 'loading at', self.destination.name)
        self.load = self.control.transport_load(self)
        self.load = 24

    def load_for_hub(self):
        self.control.load_for_hub(self, HUBS[self.hub.name])

    def is_docked(self):
        # return True

        return self.control.is_transport_docked(self)

    def is_full(self):
        self.load = self.control.transport_load()
        return self.load == self.capacity

    def is_empty(self):
        # self.load = self.control.transport_load()
        return self.load == 0

    def finish(self):
        self.status = 4
