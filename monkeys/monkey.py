
class IMonkey(arcade.Sprite):
    SIZE = 48

    def __init__(self, position, sprite_path):
        super().__init__(sprite_path)

        self.width = self.height = self.SIZE

        self.position = position

        self.range = 100.0
        
        self.reload_time = 2.5 / 3.0 
        
        self.cooldown = 0.0

        self.pop_count = 0