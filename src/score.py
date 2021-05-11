class Score():
    def __init__(self, SCREEN_WIDTH=None, decrease_mode=False, points=10):
        self.value = 0
        self.x_pos = 100
        self.font_size = 25
        self.decrease_mode = decrease_mode
        self.total_hits = 0
        # The ammount of notes correctly hit in a row
        self._counter = 0
        self.rock_meter = 50
        self.points = points

    def hit(self):
        self._counter = min(self._counter + 1, 39)
        self.value += self.points * self.multiplier
        self.total_hits += 1
        self.rock_meter = min(self.rock_meter + 2, 100)

    def miss(self):
        self._counter = 0
        self.rock_meter -= 2
        if self.rock_meter <= 0:
            global done
            done = True
        else:
            done = False
        return done

    def miss_click(self):
        done = self.miss()
        self.value -= self.points * self.decrease_mode
        return done

    @property
    def counter(self):
        return self._counter + 1

    @property
    def multiplier(self):
        return 1 + self._counter // 10
