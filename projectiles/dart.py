from projectiles.projectile import IProjectile


class DartProjectile(IProjectile):
    def __init__(self, parent, direction):
        super().__init__(parent, direction, ":assets:/projectiles/placeholder.png")
        self.speed = 600.0
        self.pierce_left = 2
