from enum import Enum, auto

import arcade


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

        # MF: XY position in world
        self.position = position

        # MF: How much money it costs
        self.cost = 0
        
        # MF: How far around self.position are thing excluded from being placed 
        self.collision_radius = 10

        self.max_range = 1000

        # MF: Max range at which a tower can 'see' a bloon
        self.target_range = 100.0

        self.reload_time = 2.5 / 3.0
        self.cooldown = 0.0

        # MF: How many bloons the tower has popped
        self.pop_count = 0

        # MF: What bloon the tower targets
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
