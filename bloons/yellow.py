from bloons.bloon import IBloon
from bloons.green import GreenBloon


class YellowBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/yellow.png", t)
        self.rbe = 4
        self.speed = 192.0

    def get_children(self, track):
        return [GreenBloon(self.track_distance)]
