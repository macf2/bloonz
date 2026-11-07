from bloons.bloon import IBloon
from bloons.blue import BlueBloon


class GreenBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/green.png", t)
        self.rbe = 3
        self.speed = 108.0

    def get_children(self, track):
        return [BlueBloon(self.track_distance)]
