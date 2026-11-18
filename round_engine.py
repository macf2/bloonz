import json

rounds = [
    [{"type": "red", "count": 5, "interval": 0.2}, {"wait": 2.0}],
]


class RoundEngine:
    def __init__(self, rounds, on_spawn):
        self.rounds = rounds
        self.on_spawn = on_spawn

        self.round_index = -1
        self.event_index = 0
        self.current = None
        self.remaining = 0
        self.timer = 0
        self.active = False

    @classmethod
    def from_file(cls, path, on_spawn):
        with open(path) as f:
            rounds = json.load(f)
        return cls(rounds, on_spawn)

    # property methods
    def spawning_done(self):
        return not self.active

    def has_next_round(self):
        return self.round_index + 1 < len(self.rounds)

    def start_next_round(self):
        if self.active or not self.has_next_round():
            return False
        else:
            self.round_index += 1
            self.event_index = 0
            self.current = None
            self.remaining = 0
            self.timer = 0.0
            self.active = True
            return True

    # spawning etc
    def update(self, dt):

        self.timer -= dt

        while self.active and self.timer <= 0:
            if (
                self.current is None and not self.load_next_event()
            ):  # if there are no more events
                self.active = False  # round done
                return

            if "wait" in self.current:
                self.timer += self.current["wait"]
                self.current = None
            else:
                self.on_spawn(self.current["type"])
                self.timer += self.current["interval"]
                self.remaining -= 1

                if self.remaining <= 0:
                    self.current = None

    def load_next_event(self):
        events = self.rounds[self.round_index]
        if self.event_index >= len(events):
            return False

        self.current = events[self.event_index]
        self.event_index += 1

        if "type" in self.current:
            self.remaining = self.current["count"]

        return True
