import arcade
from pyglet.math import Vec2

from monkeys.monkey import IMonkey
from projectiles.dart import DartProjectile


class DartMonkey(IMonkey):
    def __init__(self, position):
        super().__init__(position, ':assets:/monkeys/dart.png')
        self.cost = 250
        self.collision_radius = 10

    def update(self, dt, bloons, projectiles):
        self.cooldown -= dt

        if 0.0 < self.cooldown:
            return

        target_bloon = self.target(bloons)

        if target_bloon is not None:
            direction = Vec2(*target_bloon.position) - Vec2(*self.position)
            projectiles.append(DartProjectile(self, direction))
            self.cooldown = self.reload_time
