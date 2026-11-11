import math
import random
from enum import Enum, auto

import arcade
import arcade.color as Color
import arcade.gui
import arcade.key as Key
from pyglet.math import Vec2

from bloons.black import BlackBloon
from bloons.blue import BlueBloon
from bloons.green import GreenBloon
from bloons.red import RedBloon
from bloons.white import WhiteBloon
from bloons.yellow import YellowBloon
from monkeys.bomb_tower import BombTower
from monkeys.dart import DartMonkey
from monkeys.ice import IceMonkey
from monkeys.supermonkey import SuperMonkey
from monkeys.tack_shooter import TackShooter

from track import Track
from consts import TRACK_MIN_NODES

MONKEY_TYPES = [DartMonkey, TackShooter, BombTower, IceMonkey, SuperMonkey]
BLOON_TYPES = [RedBloon, BlueBloon, GreenBloon, YellowBloon, BlackBloon, WhiteBloon]

class Stage(Enum):
    '''
        MF: 
        This represents what stage the world is in.
        
        PRE_ROUND:
        The round has not started, monkeys are idle, no bloons. 
        You can place/sell monkeys. 

        MID_ROUND: 
        You are in the middle of the round. Bloons are spawning. 
        You can place/sell monkeys. 

        This is used in the world.update() method to switch between 
        updating the pre/mid round
    '''
    PRE_ROUND = auto()
    MID_ROUND = auto()


class World(arcade.View):

    '''
        MF: 
        This class holds all the logic for the game world. 
        It is the main screen the player will be in.
        Its what you probably think of when you imagine actually 'playing the game'.
    '''

    # MF: TODO: take in a map to load, once we get map loading working
    # def __init__(self, map_to_load):
    def __init__(self):
        super().__init__()

        # MF: TODO: Load the map, and have self.track and self.background
        # Be taken from the map, instead of these defaults
        # self.load_map(map_to_load)
        self.background = arcade.load_texture(":assets:/maps/map_1/test_map_1.jpg")
        self.track = Track()

        self.bloons = arcade.SpriteList()
        self.monkeys = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()

        self.stage = Stage.PRE_ROUND
        self.round = 1
        self.money = 5000
        self.lives = 40

        self.mouse_position = Vec2()
        self.held_keys = set()

        # MF: TODO: Eventually remove this in favor of a 'round engine'
        self.spawn_phase = 0.0
        self.spawn_wait = 0.0

        self.init_ui()

    def init_ui(self):
        self.selected_monkey = None
        self.placing = None
        self.ghost = None
        self.ui = arcade.gui.UIManager()
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())

        self.money_label = anchor.add(
            arcade.gui.UILabel(
                text="",
                width=260,
                height=34,
                font_size=20,
                bold=True
            ),
            anchor_x="left",
            anchor_y="top",
            align_x=200,
            align_y=-200
        )

        self.lives_label = anchor.add(
            arcade.gui.UILabel(
                text="",
                width=260,
                height=34,
                font_size=20,
                bold=True
            ),
            anchor_x="left",
            anchor_y="top",
            align_x=200,
            align_y=-234
        )

        # MF: Start button
        self.start_button = anchor.add(
            arcade.gui.UIFlatButton(
                text="Start round",
                width=150,
                height=100
            ),
            anchor_x="left",
            align_x=100,
            anchor_y="top",
            align_y=-100,
        )
        @self.start_button.event("on_click")
        def start_button_click(_event):
            self.start_round()

        # Nico: The menu on the right that holds the buyable towers
        self.side_menu = anchor.add(
            arcade.gui.UIGridLayout(
                column_count=2,
                row_count=(len(MONKEY_TYPES)+1) // 2,
                horizontal_spacing=10,
                vertical_spacing=10,
                align_vertical="top",
                width=150,
                height=540,
                size_hint=None
            ).with_background(color=(40, 40, 40)).with_padding(all=10),
            anchor_x="right",
            anchor_y="center",
        )

        # Nico: For each tower, add an icon to the menu
        self.menu_items = []
        for i, monkey_type in enumerate(MONKEY_TYPES):
            # MF: Because each monkey is a subclass, we have to create a dummy instance
            # to get constant attributes like cost, radius, sprite path, etc
            dummy_instance = monkey_type(Vec2())

            icon = arcade.gui.UIImage(
                texture=dummy_instance.texture,
                height=48,
                width=48
            )
            label = arcade.gui.UILabel(
                text=f"${dummy_instance.cost}",
                font_size=14
            )
            buyable_tower = arcade.gui.UIBoxLayout(
                children=[icon, label]
            )

            self.side_menu.add(buyable_tower, column=i % 2, row=i // 2)
            self.menu_items.append((monkey_type, dummy_instance.cost, buyable_tower))

    def on_update(self, delta_time):
        self.update_ui()

        keys = self.held_keys

        # MF: TODO: Remove this eventually, because of the map editor
        # MF: Move the selected nodes
        dx = 0.0
        if Key.RIGHT in keys:
            dx += 1.0
        if Key.LEFT in keys:
            dx -= 1.0
        dy = 0.0
        if Key.UP in keys:
            dy += 1.0
        if Key.DOWN in keys:
            dy -= 1.0
        speed = 60 * delta_time
        self.track.move_selected(dx * speed, dy * speed)

        # MF: Per stage updates
        match self.stage:
            case Stage.PRE_ROUND:
                pass

            case Stage.MID_ROUND:
                self.update_mid_round(delta_time)

    def on_draw(self):
        self.clear()

        # Isaac: Draws Background image
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                0,
                0,
                self.window.width,
                self.window.height
            )
        )

        self.track.draw()

        self.bloons.draw(pixelated=True)
        self.monkeys.draw(pixelated=True)
        self.projectiles.draw(pixelated=True)

        # Nico: Draw the selected monkey's shoot radius
        if self.selected_monkey:
            m = self.selected_monkey
            arcade.draw_circle_outline(
                m.position.x,
                m.position.y,
                m.target_range,
                Color.YELLOW)

        # Nico: Color the ghost monkey RED if its unable to be placed
        if self.placing:
            self.ghost.position = self.mouse_position

            if self.check_if_monkey_collides_with_something(self.ghost, self.ghost.position):
                self.ghost.color = Color.RED
            else:
                self.ghost.color = Color.WHITE

            arcade.draw_sprite(self.ghost, pixelated=True)
            arcade.draw_circle_outline(
                self.ghost.position.x,
                self.ghost.position.y,
                self.ghost.target_range,
                Color.YELLOW)

        self.ui.draw()

    def update_ui(self):
        self.money_label.text = f"{self.money}"
        self.lives_label.text = f"{self.lives}"

    def go_to_title(self):
        # MF: TODO: do something about circular dependency
        from title import Title
        self.window.show_view(Title())

    def start_round(self):
        if not self.track.is_complete:
            print(f"Track needs at least {TRACK_MIN_NODES} nodes")
            return

        print("Started round")
        self.stage = Stage.MID_ROUND
        self.start_button.visible = False

    def check_if_monkey_collides_with_something(self, monkey, position):
        # MF: TODO: the +10 is just a magic number for the width of the track
        # eventuallly we are going to need something configurable per track in the map editor
        d = monkey.collision_radius + 10

        can_place = True

        # MF: Check intersection with track
        can_place &= d < self.track.distance_to(position)

        # MF: Check collision with other monkey
        can_place &= not arcade.check_for_collision_with_list(
            monkey, self.monkeys)

        return not can_place

    def try_place_monkey(self, monkey_class, position):
        monkey = monkey_class(position)

        if self.money < monkey.cost:
            return

        if self.check_if_monkey_collides_with_something(monkey, position):
            print("Too close")
        else:
            self.monkeys.append(monkey)
            self.money -= monkey.cost

    def update_mid_round(self, dt):
        if self.lives <= 0:
            print("you are dead!")
            self.go_to_title()
            return

        # MF: TODO: Eventually we are going to want a 'round engine' type of thing
        # For example: self.round_spawner.update(dt) rather than this:
        self.spawn_bloons(dt)

        self.monkeys.update(dt, self.bloons, self.projectiles)
        self.bloons.update(dt, self.track)
        self.projectiles.update(dt, self.bloons)

        self.remove_dead_entities()

    def spawn_bloons(self, dt): # Nico: right now just spawn random bloon types
        if 0 < math.sin(self.spawn_phase) and self.spawn_wait <= 0:
            # self.bloons.append(random.choice(BLOON_TYPES)(0.0))
            self.bloons.append(YellowBloon(0.0))
            self.spawn_wait = 1.0 / 6.0
        self.spawn_phase += 6.0 * dt
        self.spawn_wait -= dt



    def remove_dead_entities(self):
        for bloon in list(self.bloons):
            if bloon.dead:
                self.money += 1
                for child in bloon.get_children(self.track):
                    self.bloons.append(child)
                bloon.remove_from_sprite_lists()
            if bloon.leaked:
                self.lives -= bloon.rbe
                bloon.remove_from_sprite_lists()

        for projectile in list(self.projectiles):
            if projectile.dead:
                projectile.remove_from_sprite_lists()

    ###########################
    # MF: Unimportant callbacks

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_mouse_press(self, x, y, button, modifiers):

        # Nico: First check for deleting a monkey
        if button == arcade.MOUSE_BUTTON_RIGHT:

            hits = arcade.get_sprites_at_point((x, y), self.monkeys)

            if hits:
                monkey = hits[0]
                monkey.kill()
                self.selected_monkey = None

            return

        # Nico: Next check if clicking menu
        for monkey_type, cost, buyable_tower in self.menu_items:
            if buyable_tower.rect.point_in_rect((x, y)):
                if self.money >= cost:
                    self.placing = monkey_type
                    self.ghost = monkey_type(self.mouse_position)
                    self.ghost.alpha = 128
                    self.selected_monkey = None
                    print(self.placing)
                return

        # Nico: Otherwise try to select a monkey on the map
        hits = arcade.get_sprites_at_point((x, y), self.monkeys)
        self.selected_monkey = hits[0] if hits else None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = Vec2(x, y)

    def on_mouse_drag(self, x, y, _dx, _dy, _buttons, _modifiers):
        self.mouse_position = Vec2(x, y)

    def on_key_press(self, symbol, modifiers):
        self.held_keys.add(symbol)

        # MF: TODO: Throw this out in favor of map editor
        if Key.T == symbol:
            self.track.add_node(self.mouse_position)
        if Key.Y == symbol:
            self.track.cycle_selected()

        # MF: TODO: Eventually add a ui button for this
        if Key.O == symbol:
            print("Saving and quiting...")
            self.go_to_title()

    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.placing:
            if (x, y) not in self.side_menu.rect:
                self.try_place_monkey(self.placing, self.mouse_position)

            self.placing = None
