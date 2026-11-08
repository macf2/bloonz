
import arcade
from pathlib import Path

from track import Track

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "Bloonz Map Editor"

NODE_RADIUS = 12
SELECTION_DISTANCE = 15


class MapEditor(arcade.Window):

    def __init__(self):
        super().__init__(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE
        )

        arcade.resources.add_resource_handle(
            "assets",
            Path.cwd() / "assets"
        )

        self.background = arcade.load_texture(
            ":assets:/maps/placeholder.jpg"
        )

        self.track = Track()

        # Keep track of whether the user is dragging a node
        self.dragging = False

    def on_draw(self):
        self.clear()
    
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, self.width, self.height)
        )
    
        self.track.draw()

    def on_mouse_press(self, x, y, button, modifiers):

        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Check whether the click is close to an existing node
        for i, node in enumerate(self.track.nodes):

            dx = node.x - x
            dy = node.y - y

            distance = (dx**2 + dy**2)**0.5

            if distance <= SELECTION_DISTANCE:

                self.track.selected = i
                self.dragging = True
                return

        # If no node was clicked, add a new one
        self.track.add_node((x, y))
        self.track.selected = len(self.track.nodes) - 1

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        if self.dragging and self.track.nodes:

            self.track.move_selected(dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = False

    def on_key_press(self, symbol, modifiers):

        if symbol in (arcade.key.DELETE, arcade.key.BACKSPACE):
            self.track.delete_selected()
            self.dragging = False

def main():
    editor = MapEditor()
    arcade.run()


if __name__ == "__main__":
    main()