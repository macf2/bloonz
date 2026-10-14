from pathlib import Path
import arcade
from title import Title

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "Bloonz"

arcade.resources.add_resource_handle("assets", Path.cwd() / "assets")

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, update_rate=1 / 60)

        music = arcade.load_sound(":assets:/background_music.wav")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()


def main():
    window = Game()
    window.show_view(Title())
    arcade.run()


if __name__ == "__main__":
    main()
