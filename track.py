import math
import arcade
import arcade.color as Color
from pyglet.math import Vec2


CLOSEST_POINT_STEP = 0.05
DRAW_STEP = 0.01

# MF: TODO: Rather than having half baked paths exist and checking if they are half made,
# just dont create the path object until there are 4 points
MIN_NODES = 4


class Track:
    def __init__(self):
        self.nodes: list[Vec2] = []
        self.selected = 0

        self._cached_draw_samples = None
        self._cached_distance_check_samples = None

    @property
    def end(self):
        return len(self.nodes) - 3.0

    def _get_segment_nodes(self, t):
        i = max(0, min(math.floor(t), len(self.nodes) - 4))
        return self.nodes[i:i + 4], t - i

    def get_point_at(self, t):
        (p0, p1, p2, p3), t = self._get_segment_nodes(t)
        t2 = t * t
        t3 = t2 * t

        q1 = -t3 + 2.0 * t2 - t
        q2 = 3.0 * t3 - 5.0 * t2 + 2.0
        q3 = -3.0 * t3 + 4.0 * t2 + t
        q4 = t3 - t2
        return (p0 * q1 + p1 * q2 + p2 * q3 + p3 * q4) * 0.5

    def get_derivative_at(self, t):
        (p0, p1, p2, p3), t = self._get_segment_nodes(t)
        t2 = t * t

        dq1 = -3.0 * t2 + 4.0 * t - 1.0
        dq2 = 9.0 * t2 - 10.0 * t
        dq3 = -9.0 * t2 + 8.0 * t + 1.0
        dq4 = 3.0 * t2 - 2.0 * t
        return (p0 * dq1 + p1 * dq2 + p2 * dq3 + p3 * dq4) * 0.5

    def _generate_samples(self, step):
        steps = int(self.end / step)
        return [self.get_point_at(i * step) for i in range(steps)] + [self.get_point_at(self.end)]

    def get_draw_samples(self):
        if not self.is_complete:
            return []

        if self._cached_draw_samples is None:
            self._cached_draw_samples = self._generate_samples(DRAW_STEP)

        return self._cached_draw_samples

    def distance_to(self, position):
        if not self.is_complete:
            return math.inf

        if self._cached_distance_check_samples is None:
            self._cached_distance_check_samples = self._generate_samples(CLOSEST_POINT_STEP)

        # MF: TODO: Lerp between the two closest samples so that
        # long track segments are not choppy
        distances = [
            (sample - position).length() for sample in self._cached_distance_check_samples
            ]
        
        return min(distances)

    def draw(self):
        if self.is_complete:
            arcade.draw_line_strip(self.get_draw_samples(), (100, 100, 100), 10)

        for i, node in enumerate(self.nodes):
            color = Color.RED if i == self.selected else Color.BLUE
            arcade.draw_point(node.x, node.y, color, 10)

    def _clear_cached_samples(self):
        self._cached_draw_samples = None
        self._cached_distance_check_samples = None

    # MF: TODO: These are probably going to get removed when map editor 
    @property
    def is_complete(self):
        return MIN_NODES <= len(self.nodes)

    def add_node(self, position):
        self.nodes.append(Vec2(*position))
        self._clear_cached_samples()

    def cycle_selected(self):
        if self.nodes:
            self.selected = (self.selected + 1) % len(self.nodes)

    def move_selected(self, dx, dy):
        if self.nodes:
            self.nodes[self.selected] += Vec2(dx, dy)
            self._clear_cached_samples()
