from controller import clicker

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
        self.capacity = 0

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
        # clicker.leftclick(self.button)
        # clicker.rightclick(dest.coords)

        #DEBUG
        print(self.__hash__(), 'sending to', dest.name)

    def unload(self):
        self.load = 0

        # DEBUG
        print(self.__hash__(), 'unloading at', self.destination.name)

        #control.unload

    def load_all(self):
        self.status = 3
        # control.load

        # DEBUG
        print(self.__hash__(), 'loading at', self.destination.name)
        self.load = 24

    def is_docked(self):
        return True

        #return self.control.is_transport_docked(self)

    def is_full(self):
        return self.load == self.capacity

    def is_empty(self):
        return self.load == 0
