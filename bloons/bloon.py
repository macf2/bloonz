import arcade


class IBloon(arcade.Sprite):
    '''
        MF: 
        General interface the all bloons share
    '''

    def __init__(self, sprite_path, t):
        super().__init__(sprite_path)
        self.width = self.height = 32
        self.track_distance = t
        self.health = 2
        self.rbe = 1
        self.speed = 60.0
        self.freeze_time = 0.0
        
        self.explosion_immune = False
        self.freeze_immune = False


        # MF: Because the bloon is responsible for handling its own update, we
        # need a way of relaying certain things back to the work. Right now, 
        # the way we do this is by setting a boolean flag, then the world 
        # loops through all bloons at the end of the update step and checks these flags
        self.dead = False
        self.leaked = False

    def get_children(self, track):
        """Bloons spawned when this one is popped."""
        return []

    def offset_distance(self, track, pixels):
        """Track distance `pixels` behind this bloon, clamped at the start."""
        length = track.get_derivative_at(self.track_distance).length()
        return max(0.0, self.track_distance - pixels / length)

    def update(self, dt, track):
        if self.freeze_time:  # Nico: decrement the freezne time each frame
            self.freeze_time = max(0.0, self.freeze_time - dt)
        else:  # Nico: if freeze_time is zero then move it
            self.move_along_track(track, dt)

        if track.get_length() <= self.track_distance:
            self.leaked = True

    def move_along_track(self, track, dt):
        speed = track.get_derivative_at(self.track_distance).length()
        self.track_distance += self.speed * dt / speed
        self.position = track.get_point_at(self.track_distance)

    def pop(self, popper):
        if self.dead:
            return

        self.dead = True
        popper.pop_count += 1

    def apply_freeze(self, time):
        if self.freeze_immune:
            return
        self.freeze_time += time

    def is_frozen(self):
        if self.freeze_time > 0:
            return True
        else:
            return False
