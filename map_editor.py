import arcade.gui
import arcade
import json
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

        # Map folder
        self.map_folder = Path("assets/maps/map_1")

        # Create folder if it doesn't exist
        self.map_folder.mkdir(parents=True, exist_ok=True)

        # Load map image
        self.background = arcade.load_texture(
            str(self.map_folder / "test_map_1.jpg")
)

        self.track = Track()

        self.dragging = False

        # Load existing spline, if available
        self.load_track()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        save_button = arcade.gui.UIFlatButton(
            text="Save Track",
            width=120,
            height=40
        )

        @save_button.event("on_click")
        def on_click(event):
            self.save_track()

        anchor = arcade.gui.UIAnchorLayout()

        anchor.add(
            save_button,
            anchor_x="left",
            anchor_y="top",
            align_x=20,
            align_y=-20
        )

        self.ui_manager.add(anchor)

    # Save that map and spline path
    def save_track(self):
        data = {
            "points": [
                [node.x / self.width, node.y / self.height]
                for node in self.track.nodes
            ]
        }

        file_path = self.map_folder / "track.json"

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("Track saved!")

    
    def load_track(self):
        file_path = self.map_folder / "track.json"


    def on_draw(self):
        self.clear()
    
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, self.width, self.height)
        )
    
        self.track.draw()
        self.ui_manager.draw()

    def on_close(self):
        self.ui_manager.disable()
        super().on_close()

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