import arcade
from pyglet.math import Vec2


class IProjectile(arcade.Sprite):
    def __init__(self, parent, direction, sprite_path):
        super().__init__(sprite_path)
        self.width = self.height = 10
        self.position = parent.position

        self.parent = parent
        self.direction = Vec2(*direction).normalize()
        self.speed = 600.0
        self.pierce_left = 1
        self.dead = False

    def update(self, dt, bloons):
        if self.dead:
            return

        self.position += self.direction * self.speed * dt

        if self.is_off_screen():
            self.dead = True
            return

        for bloon in arcade.check_for_collision_with_list(self, bloons):
            if bloon.dead:
                continue

            self.on_hit(bloon, bloons)

            if self.pierce_left <= 0:
                self.dead = True
                return

    def on_hit(self, bloon, bloons):
        bloon.pop(self.parent)
        self.pierce_left -= 1

    def is_off_screen(self):
        window = arcade.get_window()
        on_screen = True
        on_screen &= 0 <= self.center_x <= window.width
        on_screen &= 0 <= self.center_y <= window.height
        return not on_screen
