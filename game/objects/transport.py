class Transport:
    """
    statuses
    # 0 -idle
    # 1 - flying
    # 2 - doxked
    # 3 - loaded
    # 8 - unloading to hub
    # 9 - unloading
    """
    def __init__(self, button):
        self.button = button,
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