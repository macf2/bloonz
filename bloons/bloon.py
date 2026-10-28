


class IBloon(arcade.Sprite):
    SIZE = 32

    def __init__(self, sprite_path, t):
        super().__init__(sprite_path)
        self.width = self.height = self.SIZE
        self.track_distance = t
        self.health = 2

    def move_along_track(self, track):
        pass