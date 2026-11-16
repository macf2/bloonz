import arcade
import arcade.gui


class WinScreen(arcade.View):
    '''
        Shown after the last round is cleared.
    '''

    def __init__(self, lives_left):
        super().__init__(background_color=(20, 40, 20))

        self.ui = arcade.gui.UIManager()
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        box = anchor.add(arcade.gui.UIBoxLayout(space_between=20))

        box.add(arcade.gui.UILabel(text="You Win!", font_size=48, bold=True))
        box.add(arcade.gui.UILabel(text=f"Lives left: {lives_left}", font_size=20))

        title_button = box.add(arcade.gui.UIFlatButton(
            text="Back to title", width=200, height=80))

        @title_button.event("on_click")
        def title_button_click(_event):
            # Imported here to avoid a circular import (title -> world -> win)
            from title import Title
            self.window.show_view(Title())

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
