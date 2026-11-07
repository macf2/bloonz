from pathlib import Path
import arcade
from title import Title
from consts import GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_TITLE 

arcade.resources.add_resource_handle("assets", Path.cwd() / "assets")


class Game(arcade.Window):
    '''
        MF: 
        This is the game class.
        This really doesnt do anything. 
        All the logic happens in World and Title.
    '''
    def __init__(self):
        super().__init__(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, GAME_WINDOW_TITLE, update_rate=1 / 60)

        # MF: TODO: Add music when making the finishing touches to game
        # music = arcade.load_sound(":assets:/music/placeholder.wav")

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()


def main():
    window = Game()
    window.show_view(Title())
    arcade.run()


if __name__ == "__main__":
    main()
