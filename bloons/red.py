from bloons.bloon import IBloon


class RedBloon(IBloon):
    def __init__(self, t):
        super().__init__(":assets:/bloons/red.png", t)
        self.rbe = 1
        self.speed = 60.0
