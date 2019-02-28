from pygame import *

import maps


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WALL_LENGTH = 32
WALL_COLOR = "#662218"


class MainScene:

    def __init__(self):
        init()
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption("Ghost&Hunter")
        self.timer = time.Clock()

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit

    def draw_map(self):
        x = y = 0
        for row in maps.hotel_map:
            for col in row:
                if col == '-':
                    wall = Surface((WALL_LENGTH, WALL_LENGTH))
                    wall.fill(Color(WALL_COLOR))
                    self.screen.blit(wall, (x, y))
                x += WALL_LENGTH
            y += WALL_LENGTH
            x = 0

    def mainloop(self):
        while True:
            self.check_events()
            self.draw_map()
            self.timer.tick(60)
            display.update()


if __name__ == '__main__':
    game = MainScene()
    game.mainloop()