
from monkeys.monkey import IMonkey

class DartMonkey(IMonkey):
    def __init__(self, position):
        super().__init__(':assets:/monkeys/dart.png')


    def on_update(self, bloons, darts, dt):
        self.cooldown -= dt

        if 0.0 < self.cooldown:
            return

        # MF: TODO: add more than target closest
        closest = arcade.get_closest_sprite(self, self.bloons)
        
        if closest is None:
            return
        bloon, distance = closest

        in_range = distance <= self.range
        if in_range:
            direction = Vec2(*bloon.position) - Vec2(*self.position)
            self.darts.append(Dart(self, direction))
            self.cooldown = self.reload_time