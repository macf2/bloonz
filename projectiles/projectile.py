


class IProjectile(arcade.Sprite):
    SIZE = 10

    def __init__(self, parent, sprite_path):
        super().__init__(sprite_path)
        self.width = self.height = self.SIZE
        self.position = parent.position

        self.parent = parent
        self.velocity = Vec2(*direction).normalize() * DART_SPEED
        self.pierce_left = 2
