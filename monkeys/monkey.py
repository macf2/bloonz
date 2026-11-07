import arcade
from enum import Enum, auto


class MonkeyTargetMode(Enum):
    '''
        MF: 
        Hold options for when the monkey is targeting 
        the first, closest, strongest, or last
        bloon in its radius
    '''
    FIRST = auto(),
    CLOSE = auto(),
    STRONG = auto(),
    LAST = auto()


class IMonkey(arcade.Sprite):
    '''
        MF: 
        General interface that all the monkeys share
    '''

    def __init__(self, position, sprite_path):
        super().__init__(sprite_path)
        self.width = self.height = 48
        self.position = position
        self.cost = 0
        self.collision_radius = 10
        self.target_range = 100.0
        self.reload_time = 2.5 / 3.0
        self.cooldown = 0.0
        self.pop_count = 0
        self.targeting_mode = MonkeyTargetMode.CLOSE

    def update(self, dt, bloons, projectiles):
        pass

    def target(self, bloons):
        match self.targeting_mode:

            case MonkeyTargetMode.CLOSE:
                result = arcade.get_closest_sprite(self, bloons)

                if result is not None:
                    bloon, distance = result

                    if distance < self.target_range:
                        return bloon

                return None

            case MonkeyTargetMode.FIRST:
                max_t = -10000000
                b = None
                for bloon in bloons:
                    d = (bloon.position - self.position).length()
                    if d < self.target_range:
                        if bloon.track_distance > max_t:
                            max_t = bloon.track_distance
                            b = bloon
                return b

            case MonkeyTargetMode.LAST:
                min_t = 10000000
                b = None
                for bloon in bloons:
                    d = (bloon.position - self.position).length()
                    if d < self.target_range:
                        if bloon.track_distance < min_t:
                            min_t = bloon.track_distance
                            b = bloon
                return b

            case MonkeyTargetMode.STRONG:
                b = None
                max_rbe = -100000000
                for bloon in bloons:
                    d = (bloon.position - self.position).length()
                    if d < self.target_range:
                        if bloon.rbe > max_rbe:
                            max_rbe = bloon.rbe
                            b = bloon
                return b
