from init import *
import time
class Orbit:
    def __init__(self, screen):
        self.orbit = []
        self.screen = screen

    def draw(self, index_finger_tip_x, index_finger_tip_y):
        now = time.time_ns() / 100000
        self.orbit = list(filter(lambda x: now - x[0] <= 90000, self.orbit))

        for i in range(1, len(self.orbit)):
            line_width = int(ph(0.0003) * (self.orbit[i][0] + 100 - now))
            line_width = max(line_width, 1)
            pygame.draw.aaline(self.screen, (255, 255, 255),
                             self.orbit[i - 1], self.orbit[i],
                             line_width)