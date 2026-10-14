import math
from enum import Enum, auto

import arcade
import arcade.gui
from pyglet.math import Vec2

from sprites import Bloon, BloonType, Dart, Monkey, MonkeyType
from track import MIN_NODES, Track

class Stage(Enum):
    PRE_ROUND = auto()
    MID_ROUND = auto()

class World(arcade.View):
    def __init__(self):
        super().__init__(background_color=(70, 140, 60))

        self.track = Track()
        self.bloons = arcade.SpriteList()
        self.monkeys = arcade.SpriteList()
        self.darts = arcade.SpriteList()

        self.stage = Stage.PRE_ROUND
        self.round = 1
        self.money = 650
        self.lives = 40

        self.mousePosition = Vec2()
        self.held_keys = set()

        self.spawn_phase = 0.0
        self.spawn_wait = 0.0

        self.hud = arcade.Text(
            "", 10, self.window.height - 30, arcade.color.WHITE, 16)

        self.ui = arcade.gui.UIManager()
        anchor = self.ui.add(arcade.gui.UIAnchorLayout())
        self.start_button = anchor.add(
            arcade.gui.UIFlatButton(text="Start round", width=150, height=100),
            anchor_x="left", align_x=100,
            anchor_y="top", align_y=-100,
        )

        @self.start_button.event("on_click")
        def on_click(event):
            self.start_round()

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mousePosition = Vec2(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mousePosition = Vec2(x, y)

    def on_key_press(self, symbol, modifiers):
        self.held_keys.add(symbol)
    
        if arcade.key.I == symbol:
            self.try_place_monkey(MonkeyType.DART, self.mousePosition)

        if arcade.key.T == symbol:
            self.track.add_node(self.mousePosition)

        if arcade.key.Y == symbol:
            self.track.cycle_selected()

        if arcade.key.O == symbol:
            print("Saving and quiting...")
            self.go_to_title()

    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)

    def go_to_title(self):
        # MF: TODO: do something about circular dependency
        from title import Title
        self.window.show_view(Title())

    def start_round(self):
        if len(self.track.nodes) < MIN_NODES:
            print(f"Track needs at least {MIN_NODES} nodes")
            return

        print("Started round")
        self.stage = Stage.MID_ROUND
        self.start_button.visible = False

    def try_place_monkey(self, type, position):
        if self.money < type.cost:
            return

        d = type.radius + 10
        if d < self.track.distance_to(position):
            self.monkeys.append(Monkey(position, type))
            self.money -= type.cost
        else:
            print("Too close")

    def on_update(self, dt):
        keys = self.held_keys

        # MF: Move the selected nodes
        dx = 0.0
        if arcade.key.RIGHT in keys:
            dx += 1.0
        if arcade.key.LEFT in keys:
            dx -= 1.0

        dy = 0.0
        if arcade.key.UP in keys:
            dy += 1.0
        if arcade.key.DOWN in keys:
            dy -= 1.0

        speed = 60 * dt
        self.track.move_selected(dx * speed, dy * speed)

        # MF: Per stage updates
        match self.stage:
            case Stage.PRE_ROUND:
                pass

            case Stage.MID_ROUND:
                self.update_mid_round(dt)

    def update_mid_round(self, dt):
        self.spawn_bloons(dt)

        self.bloons.update(dt)
        for bloon in list(self.bloons):
            if bloon.escaped:
                self.lives -= bloon.type.rbe
                bloon.remove_from_sprite_lists()

        if self.lives <= 0:
            print("you are dead!")
            self.go_to_title()
            return

        self.shoot_monkeys(dt)

        self.darts.update(dt)
        for dart in list(self.darts):
            self.hit_bloons(dart)

    def spawn_bloons(self, dt):
        if 0 < math.sin(self.spawn_phase) and self.spawn_wait <= 0:
            self.bloons.append(Bloon(self.track, BloonType.RED))
            self.spawn_wait = 1.0 / 6.0

        self.spawn_phase += 6.0 * dt
        self.spawn_wait -= dt

    def shoot_monkeys(self, dt):
        for monkey in self.monkeys:
            monkey.cooldown -= dt

            # MF: TODO: add more than  Target closest
            closest = arcade.get_closest_sprite(monkey, self.bloons)
            if closest is None:
                continue

            bloon, distance = closest
            if distance <= monkey.range and monkey.cooldown <= 0.0:
                direction = Vec2(*bloon.position) - Vec2(*monkey.position)
                self.darts.append(Dart(monkey, direction))
                monkey.cooldown = monkey.reload_time

    def hit_bloons(self, dart):

        # MF:  lazily remove dart??
        if not 0 <= dart.center_x <= self.window.width or not 0 <= dart.center_y <= self.window.height:
            dart.remove_from_sprite_lists()
            return

        for bloon in arcade.check_for_collision_with_list(dart, self.bloons):
            self.money += bloon.type.rbe
            bloon.remove_from_sprite_lists()

            dart.pierce_left -= 1
            if dart.pierce_left <= 0:
                dart.remove_from_sprite_lists()
                return

    def on_draw(self):
        self.clear()

        if self.track.line_points:
            arcade.draw_line_strip(self.track.line_points, (100, 100, 100), 10)
        for i, node in enumerate(self.track.nodes):
            color = arcade.color.RED if i == self.track.selected else arcade.color.BLUE
            arcade.draw_point(node.x, node.y, color, 10)

        self.bloons.draw(pixelated=True)
        self.monkeys.draw(pixelated=True)
        self.darts.draw(pixelated=True)

        self.hud.text = f"Round {self.round}   ${self.money}   Lives {self.lives}"
        self.hud.draw()
        self.ui.draw()
