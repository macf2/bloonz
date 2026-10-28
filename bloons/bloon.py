import arcade


class IBloon(arcade.Sprite):
    def __init__(self, sprite_path, t):
        super().__init__(sprite_path)
        self.width = self.height = 32
        self.track_distance = t
        self.health = 2
        self.rbe = 1
        self.speed = 60.0
        self.dead = False

    def update(self, dt, track):
        self.move_along_track(track, dt)

    def move_along_track(self, track, dt):
        speed = track.get_derivative_at(self.track_distance).length()
        self.track_distance += self.speed * dt / speed
        self.position = track.get_point_at(self.track_distance)

    def pop(self, popper):
        if self.dead:
            return

        self.dead = True
        popper.pop_count += 1
