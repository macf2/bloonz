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
        self.freeze_time = 0.0

    def update(self, dt, track):
        if self.freeze_time: #decrement the freezne time each frame
            self.freeze_time =max(0.0, self.freeze_time - dt) 
        else: #if freeze_time is zero then move it
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
    def apply_freeze(self, time):
        self.freeze_time += time
        
    def is_frozen(self):
        if self.freeze_time > 0:
            return True
        else:
            return False
        
    
