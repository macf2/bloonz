from bloons.bloon import IBloon
from bloons.red import RedBloon


class BlueBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/blue.png", t)
        self.rbe = 2
        self.speed = 84.0

    def get_children(self, track):
        return [RedBloon(self.track_distance)]
