import arcade
import arcade.gui

from world import World

# MF: TODO: Eventually we will have a function called like get_maps that will
# query the firebase and add to this
MAPS = [
    'save 1',
    'save 2',
    "Bob's custom map",
    'Jimmys map v 3.0'
]


class Title(arcade.View):
    '''
        MF: 
        This is the title view.
        This classes hold all the logic for when the game is in the title. 
        Its responsible for selecting maps and transitioning to the world.
        It is the initial landing screen for the game.
    '''

    def __init__(self):
        super().__init__(background_color=(20, 20, 40))

        # MF: TODO: this is just the defaultt map, maybe make it so that the user cannot
        # play without selecting a map, EX: the button doesnt show up until a map is
        # selected
        self.selected_map = MAPS[0]

        self.ui = arcade.gui.UIManager()
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        box = anchor.add(arcade.gui.UIBoxLayout(space_between=20))

        # MF: Map dropdown menu
        map_dropdown = box.add(arcade.gui.UIDropdown(
            default=self.selected_map,
            options=MAPS,
            width=300,
            height=50
        ))
        @map_dropdown.event('on_change')
        def on_map_change(event):
            self.selected_map = event.new_value

        # MF: Play button
        play_button = box.add(arcade.gui.UIFlatButton(
            text="Play Selected", width=200, height=100))
        @play_button.event("on_click")
        def play_button_click(_event):
            # MF: TODO: Pass in thte seleced map to he world, once we get map loading working
            # self.window.show_view(World(self.seleced_map))
            self.window.show_view(World())

        # MF: Map editor button
        map_editor_button = box.add(arcade.gui.UIFlatButton(
            text="Map Editor", width=200, height=100))
        @map_editor_button.event("on_click")
        def map_editor_button_click(_event):
            print("trying to enter map editor")
            # self.window.show_view(MapEditor())

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
