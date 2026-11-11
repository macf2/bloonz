import math

import arcade

from monkeys.monkey import IMonkey
from projectiles.tack import TackProjectile


class TackShooter(IMonkey):
    def __init__(self, position):
        super().__init__(position, ":assets:/monkeys/tack.png") 
        self.cost = 325
        self.collision_radius = 10
        self.target_range = 75
        self.darts_per_shot = 8
        self.reload_time = 1.375
        
    def update(self, dt, bloons, projectiles):
        self.cooldown -= dt
        if 0.0 < self.cooldown:
            return

        
        closest = arcade.get_closest_sprite(self, bloons)
        
        if closest is None:
            return
        bloon, distance = closest

        in_range = distance <= self.range
        if in_range:
            for i in range(self.darts_per_shot):
                degree =  i * 360 / self.darts_per_shot 
                rad = math.radians(degree)
                direction = (math.sin(rad), math.cos(rad))
                projectiles.append(TackProjectile(self, direction))
            
            self.cooldown = self.reload_time        
        
        