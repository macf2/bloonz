import math
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
        self._line_points = None

    @property
    def end(self):
        return len(self.nodes) - 3.0

    def add_node(self, position):
        self.nodes.append(Vec2(*position))
        self._line_points = None

    def cycle_selected(self):
        if self.nodes:
            self.selected = (self.selected + 1) % len(self.nodes)

    def move_selected(self, dx, dy):
        if self.nodes:
            self.nodes[self.selected] += Vec2(dx, dy)
            self._line_points = None

    def _segment(self, t):
        i = max(0, min(math.floor(t), len(self.nodes) - 4))
        return self.nodes[i:i + 4], t - i

    def point(self, t):
        (p0, p1, p2, p3), t = self._segment(t)
        t2 = t * t
        t3 = t2 * t

        q1 = -t3 + 2.0 * t2 - t
        q2 = 3.0 * t3 - 5.0 * t2 + 2.0
        q3 = -3.0 * t3 + 4.0 * t2 + t
        q4 = t3 - t2
        return (p0 * q1 + p1 * q2 + p2 * q3 + p3 * q4) * 0.5

    def derivative(self, t):
        (p0, p1, p2, p3), t = self._segment(t)
        t2 = t * t

        dq1 = -3.0 * t2 + 4.0 * t - 1.0
        dq2 = 9.0 * t2 - 10.0 * t
        dq3 = -9.0 * t2 + 8.0 * t + 1.0
        dq4 = 3.0 * t2 - 2.0 * t
        return (p0 * dq1 + p1 * dq2 + p2 * dq3 + p3 * dq4) * 0.5

    def _sample(self, step):
        steps = int(self.end / step)
        return [self.point(i * step) for i in range(steps)] + [self.point(self.end)]

    @property
    def line_points(self):
        if len(self.nodes) < MIN_NODES:
            return []

        if self._line_points is None:
            self._line_points = self._sample(DRAW_STEP)

        return self._line_points

    def distance_to(self, position):
        if len(self.nodes) < MIN_NODES:
            return math.inf

        # MF: TODO: Lerp between the two closest samples so that
        # long track segments are not choppy
        samples = self._sample(CLOSEST_POINT_STEP)
        distances = [(sample - position).length() for sample in samples]
        return min(distances)
