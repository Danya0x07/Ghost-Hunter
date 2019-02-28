from pygame import *

import maps


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
WALL_LENGTH = 32
WALL_COLOR = "#662218"


class Direction:
    def __init__(self):
        self.w = False
        self.s = False
        self.a = False
        self.d = False


class Hunter(sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32
    MOVE_SPEED = 5
    COLOR = "#AAAAAA"

    def __init__(self, x, y):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.x_vel = 0
        self.y_vel = 0
        self.dir = Direction()
        self.image = Surface((Hunter.WIDTH, Hunter.HEIGHT))
        self.image.fill(Color(Hunter.COLOR))
        self.rect = Rect(x, y, Hunter.WIDTH, Hunter.HEIGHT)

    def update(self):
        if self.dir.w:
            self.y_vel = -Hunter.MOVE_SPEED
        if self.dir.s:
            self.y_vel = Hunter.MOVE_SPEED
        if self.dir.a:
            self.x_vel = -Hunter.MOVE_SPEED
        if self.dir.d:
            self.x_vel = Hunter.MOVE_SPEED
        if not (self.dir.w or self.dir.s):
            self.y_vel = 0
        if not (self.dir.a or self.dir.d):
            self.x_vel = 0
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class MainScene:

    def __init__(self, hunter):
        init()
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption("Ghost&Hunter")
        self.bg = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.fill(Color('#000077'))
        self.timer = time.Clock()
        self.hunter = hunter

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN:
                if e.key == K_w: self.hunter.dir.w = True
                if e.key == K_s: self.hunter.dir.s = True
                if e.key == K_a: self.hunter.dir.a = True
                if e.key == K_d: self.hunter.dir.d = True
            if e.type == KEYUP:
                if e.key == K_w: self.hunter.dir.w = False
                if e.key == K_s: self.hunter.dir.s = False
                if e.key == K_a: self.hunter.dir.a = False
                if e.key == K_d: self.hunter.dir.d = False

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
            self.screen.blit(self.bg, (0, 0))
            self.draw_map()
            self.hunter.update()
            self.hunter.draw(self.screen)
            self.timer.tick(60)
            display.update()


if __name__ == '__main__':
    hunter = Hunter(0, 0)
    game = MainScene(hunter)
    game.mainloop()