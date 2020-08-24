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
        self.button = button,
        self.control = control_interface
        self.status = 0
        self.destination = ''
        self.visited = []
        self.hub = ''
        self.full = False

    def reset_task(self):
        self.status = 0
        self.destination = ''
        self.visited = []
        self.hub = ''
        self.full = False
        print(self.__hash__(), 'reset')

    def send_to_dest(self, dest):
        print(self.__hash__(), 'sending to', dest.name)
        self.status = 1
        self.destination = dest.name

        # clicker.leftclick(self.button)
        # clicker.rightclick(dest.coords)

    def unload(self):
        print(self.__hash__(), 'unloading')

        #control.unload

    def load(self):
        print(self.__hash__(), 'loading')
        #control.load

    def is_docked(self):
        return True

    def is_full(self):
        return True

    def is_empty(self):
        return True
