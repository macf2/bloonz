import arcade
import arcade.gui

from world import World

class Title(arcade.View):
    def __init__(self):
        super().__init__(background_color=(20, 20, 40))

        self.ui = arcade.gui.UIManager()
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        play_button = anchor.add(arcade.gui.UIFlatButton(
            text="Save 1", width=200, height=100))

        @play_button.event("on_click")
        def on_click(event):
            print("SAVE 1 SELECTED")
            self.window.show_view(World())

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
