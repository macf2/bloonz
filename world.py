import math
from enum import Enum, auto

import arcade
import arcade.gui
import arcade.color as Color
import arcade.key as Key

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

        self.init_ui()

    def init_ui(self):
        self.selectedMonkey = None
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
        def on_click(event):
            self.start_round()
            
        #side side menu on the right:
        self.side_menu = anchor.add(
            arcade.gui.UIGridLayout(
                column_count = 2,
                row_count = (len(MonkeyType)+1) // 2,
                horizontal_spacing = 10,
                vertical_spacing = 10,
                align_vertical= "top",
                width = 150,
                height = 540,
                size_hint = None    
            ).with_background(color = (40,40,40)).with_padding(all=10),
            anchor_x = "right",
            anchor_y = "center",
        )
        #adding an icon to the menu for each tower
        self.menu_items = []
        for i,  type in enumerate(MonkeyType):
            
            icon = arcade.gui.UIImage(
                texture = arcade.load_texture(":assets:/dart_monkey.png"),
                height=48,
                width = 48
            )
            label = arcade.gui.UILabel(
                text = f"${type.cost}",
                font_size = 14
            )
            
            buyable_tower = arcade.gui.UIBoxLayout(
                children = [icon, label]
                
            )
            
            self.side_menu.add(buyable_tower, column = i % 2, row = i // 2)
            
            self.menu_items.append((type, buyable_tower))
            
            

    def on_update(self, dt):
        self.update_ui()

        keys = self.held_keys

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

        speed = 60 * dt
        self.track.move_selected(dx * speed, dy * speed)

        # MF: Per stage updates
        match self.stage:
            case Stage.PRE_ROUND:
                pass

            case Stage.MID_ROUND:
                self.update_mid_round(dt)

    def on_draw(self):
        self.clear()

        if self.track.line_points:
            arcade.draw_line_strip(self.track.line_points, (100, 100, 100), 10)
        for i, node in enumerate(self.track.nodes):
            color = Color.RED if i == self.track.selected else Color.BLUE
            arcade.draw_point(node.x, node.y, color, 10)

        self.bloons.draw(pixelated=True)
        self.monkeys.draw(pixelated=True)
        self.darts.draw(pixelated=True)

        if self.selectedMonkey:
            m = self.selectedMonkey
            arcade.draw_circle_outline(
                m.position.x,
                m.position.y,
                m.range,
                Color.YELLOW)
        if self.placing:
            self.ghost.position = self.mousePosition
            too_close = self.track.distance_to(self.mousePosition) <= self.placing.radius + 10
            if too_close:
                self.ghost.color = Color.RED
            else:
                self.ghost.color = Color.WHITE
            
            arcade.draw_sprite(self.ghost,pixelated = True)
            arcade.draw_circle_outline(
                self.ghost.position.x,
                self.ghost.position.y,
                self.ghost.range,
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

    def update_mid_round(self, dt):

        if self.lives <= 0:
            print("you are dead!")
            self.go_to_title()
            return

        self.spawn_bloons(dt)
        self.update_monkeys(dt)
        self.update_bloons(dt)
        self.update_darts(dt)

    def spawn_bloons(self, dt):
        if 0 < math.sin(self.spawn_phase) and self.spawn_wait <= 0:
            self.bloons.append(Bloon(BloonType.RED, 0.0))
            self.spawn_wait = 1.0 / 6.0
        self.spawn_phase += 6.0 * dt
        self.spawn_wait -= dt

    def update_monkeys(self, dt):
        for monkey in list(self.monkeys):
            monkey.cooldown -= dt

            if 0.0 < monkey.cooldown:
                continue

            # MF: TODO: add more than target closest
            closest = arcade.get_closest_sprite(monkey, self.bloons)
            
            if closest is None:
                continue
            bloon, distance = arcade.get_closest_sprite(monkey, self.bloons)

            if bloon:
                in_range = distance <= monkey.range
                if in_range:
                    direction = Vec2(*bloon.position) - Vec2(*monkey.position)
                    self.darts.append(Dart(monkey, direction))
                    monkey.cooldown = monkey.reload_time

    def update_bloons(self, dt):
        for bloon in list(self.bloons):
            speed = self.track.derivative(bloon.track_distance).length()
            bloon.track_distance += bloon.type.speed * dt / speed
            bloon.position = self.track.point(bloon.track_distance)

    def update_darts(self, dt):
        for dart in list(self.darts):
            dart.position += dart.velocity * dt

            on_screen = True
            on_screen &= 0 <= dart.center_x <= self.window.width
            on_screen &= 0 <= dart.center_y <= self.window.height
            if not on_screen:
                dart.remove_from_sprite_lists()

            for bloon in arcade.check_for_collision_with_list(dart, self.bloons):
                self.money += bloon.type.rbe
                bloon.remove_from_sprite_lists()

                dart.parent.pop_count += 1
                dart.pierce_left -= 1

                if dart.pierce_left <= 0:
                    dart.remove_from_sprite_lists()
                    break

    ###########################
    # MF: Unimportant callbacks

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_mouse_press(self, x, y, button, modifiers):
        #check to see if clicking menu
        for monkey_type, buyable_tower in self.menu_items:
            if buyable_tower.rect.point_in_rect((x,y)):
                if self.money >= monkey_type.cost:
                    self.placing = monkey_type
                    self.ghost = Monkey(self.mousePosition, monkey_type)
                    self.ghost.alpha = 128
                    self.selectedMonkey = None
                    print(self.placing)
                return
        #otherwise selecting a monkey on the map
        hits = arcade.get_sprites_at_point((x, y), self.monkeys)
        self.selectedMonkey = hits[0] if hits else None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mousePosition = Vec2(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mousePosition = Vec2(x, y)

    def on_key_press(self, symbol, modifiers):
        self.held_keys.add(symbol)

        # if Key.I == symbol:
        #     self.try_place_monkey(MonkeyType.DART, self.mousePosition)

        if Key.T == symbol:
            self.track.add_node(self.mousePosition)

        if Key.Y == symbol:
            self.track.cycle_selected()

        if Key.O == symbol:
            print("Saving and quiting...")
            self.go_to_title()

    def on_key_release(self, symbol, modifiers):
        self.held_keys.discard(symbol)
        
    def on_mouse_release(self, x, y, button, modifiers):
        if self.placing:
            if (x,y) not in self.side_menu.rect:
                self.try_place_monkey(self.placing, self.mousePosition)
                
            self.placing = None
            self.placing = None
