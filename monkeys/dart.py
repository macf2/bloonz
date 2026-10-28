import arcade
from pyglet.math import Vec2

from monkeys.monkey import IMonkey
from projectiles.dart import DartProjectile


class DartMonkey(IMonkey):
    def __init__(self, position):
        super().__init__(position, ':assets:/monkeys/dart.png')
        self.cost = 250
        self.radius = 10

    def update(self, dt, bloons, projectiles):
        self.cooldown -= dt

        if 0.0 < self.cooldown:
            return

        # MF: TODO: add more than target closest, also make a common method for this in IMonkey
        closest = arcade.get_closest_sprite(self, bloons)
        
        if closest is None:
            return
        bloon, distance = closest

        in_range = distance <= self.range
        if in_range:
            direction = Vec2(*bloon.position) - Vec2(*self.position)
            projectiles.append(DartProjectile(self, direction))
            self.cooldown = self.reload_time
