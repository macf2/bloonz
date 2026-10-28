import arcade
from enum import Enum, auto


class MonkeyTargetMode(Enum):
    FIRST = auto(),
    CLOSE = auto(),
    STRONG = auto(),
    LAST = auto()


class IMonkey(arcade.Sprite):
    def __init__(self, position, sprite_path):
        super().__init__(sprite_path)
        self.width = self.height = 48
        self.position = position
        self.cost = 0
        self.radius = 10
        self.range = 100.0
        self.reload_time = 2.5 / 3.0
        self.cooldown = 0.0
        self.pop_count = 0
        self.targeting_mode = MonkeyTargetMode.FIRST

    def update(self, dt, bloons, projectiles):
        pass

    def target_bloon():
        pass

    def find_closest_bloon():
        pass
