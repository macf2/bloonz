from bloons.bloon import IBloon
from bloons.yellow import YellowBloon


class WhiteBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/white.png", t)
        self.rbe = 11
        self.speed = 120.0
        self.freeze_immune = True

    def get_children(self, track):
        return [YellowBloon(self.track_distance),
                YellowBloon(self.offset_distance(track, 6))]
