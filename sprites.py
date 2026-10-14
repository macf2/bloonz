from enum import Enum
import arcade
from pyglet.math import Vec2


DART_SPEED = 600.0  # pixels/sec


class BloonType(Enum):
    RED = 1
    BLUE = 2
    MOAB = 3

    @property
    def rbe(self):
        rbe_from_type = {
            BloonType.RED: 1,
            BloonType.BLUE: 2,
            BloonType.MOAB: 616
        }
        return rbe_from_type[self]

    @property
    def speed(self):
        return 60.0


class Bloon(arcade.Sprite):
    SIZE = 32

    def __init__(self, track, type):
        super().__init__(":assets:/red_bloon.png")
        self.width = self.height = self.SIZE

        self.track = track
        self.type = type
        self.track_distance = 0.0
        self.health = 2
        self._place_on_track()

    @property
    def escaped(self):
        return self.track.end <= self.track_distance

    def _place_on_track(self):
        self.position = self.track.point(self.track_distance)

    def update(self, dt):
        speed = self.track.derivative(self.track_distance).length()
        self.track_distance += self.type.speed * dt / speed
        self._place_on_track()


class MonkeyType(Enum):
    DART = 1

    @property
    def cost(self):
        return {MonkeyType.DART: 250}[self]

    @property
    def radius(self):
        return {MonkeyType.DART: 10}[self]


class Monkey(arcade.Sprite):
    SIZE = 48

    def __init__(self, position, monkey_type=MonkeyType.DART):
        super().__init__(":assets:/dart_monkey.png")
        self.width = self.height = self.SIZE
        self.position = position

        self.type = monkey_type
        self.range = 100.0
        self.reload_time = 2.5 / 3.0 
        self.cooldown = 0.0


class Dart(arcade.Sprite):
    SIZE = 10

    def __init__(self, parent, direction):
        super().__init__(":assets:/placeholder.png")
        self.width = self.height = self.SIZE
        self.position = parent.position

        self.parent = parent
        self.velocity = Vec2(*direction).normalize() * DART_SPEED
        self.pierce_left = 2

    def update(self, dt):
        self.position += self.velocity * dt
