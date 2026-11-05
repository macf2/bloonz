from projectiles.projectile import IProjectile


class TackProjectile(IProjectile):
    def __init__(self, parent, direction):
        super().__init__(parent, direction, ":assets:/projectiles/tack.png")
        self.scale = .075
        self.speed = 450
        self.pierce_left = 1
