from projectiles.projectile import IProjectile


class FreezeProjectile(IProjectile):
    
    def __init__(self, parent, direction):
        super().__init__(parent, direction, ":assets:/projectiles/freeze-orb.png")
        self.scale = .075
        self.speed = 165
        self.pierce_left = 1
        self.blast_radius = 50
        self.max_targets = 20
        self.max_distance = parent.range * 1.65
        self.freeze_time = 1.25

    def on_hit(self,bloon,bloons ):
        hits = 0
        for target in bloons:
            if hits < self.max_targets:
                distance = (self.center_x - target.center_x )** 2 + (self.center_y - target.center_y) ** 2
                if distance <= self.blast_radius ** 2:
                    target.apply_freeze(self.freeze_time)
                    hits += 1
        self.dead = True
            
            
        
        
        


