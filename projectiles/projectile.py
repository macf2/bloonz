import arcade
from pyglet.math import Vec2


class IProjectile(arcade.Sprite):
    '''
        MF: 
        General interface that all projectiles share
    '''
    def __init__(self, parent, direction, sprite_path):
        super().__init__(sprite_path)
        self.width = self.height = 10
        self.position = parent.position

        self.parent = parent
        self.direction = Vec2(*direction).normalize()
        self.speed = 600.0
        self.pierce_left = 1
        self.dead = False
        self.spawn_position = parent.position
        self.distance_traveled = 0

        self.max_distance = 1.3 * parent.max_range

        self.life_timer = 0.25

    def update(self, dt, bloons):
        if self.dead:
            return

        self.position += self.direction * self.speed * dt
        self.distance_traveled += self.speed * dt

        if self.is_off_screen():
            self.dead = True
            return
        if self.distance_traveled >= self.max_distance:
            self.dead = True
            return

        for bloon in arcade.check_for_collision_with_list(self, bloons):
            if bloon.dead:
                continue

            self.on_hit(bloon, bloons)

            if self.pierce_left <= 0:
                self.dead = True
                return


        self.life_timer -= dt
        if self.life_timer < 0.0:
            self.dead = True

    def on_hit(self, bloon, bloons):
        if not bloon.is_frozen():
            bloon.pop(self.parent)
            self.pierce_left -= 1

    def is_off_screen(self):
        window = arcade.get_window()
        on_screen = True
        on_screen &= 0 <= self.center_x <= window.width
        on_screen &= 0 <= self.center_y <= window.height
        return not on_screen
