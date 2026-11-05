
import arcade
from pyglet.math import Vec2

from monkeys.monkey import IMonkey
from projectiles.freezeball import FreezeProjectile

class IceMonkey(IMonkey):
    def __init__(self, position):
        super().__init__(position, ':assets:/monkeys/ice.png')
        self.cost = 850
        self.radius = 10
        self.range = 60
        self.reload_time = 2.5

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
            projectiles.append(FreezeProjectile(self, direction))
            self.cooldown = self.reload_time

