from bloons.bloon import IBloon
from bloons.yellow import YellowBloon


class BlackBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/black.png", t)
        self.rbe = 11
        self.speed = 108.0
        self.explosion_immune = True

    def get_children(self, track):
        return [YellowBloon(self.track_distance),
                YellowBloon(self.offset_distance(track, 6))]
