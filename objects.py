from pygame import (Surface, Color, Rect)
from pygame.sprite import Sprite

from settings import *

class Direction:
    def __init__(self):
        self.w = False
        self.s = False
        self.a = False
        self.d = False


class Hunter(Sprite):
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


class Camera:

    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        targ_left, targ_top, targ_width, targ_height = target.rect
        cam_left, cam_top, cam_width, cam_height = self.state
        targ_left = SCREEN_WIDTH // 2 - targ_left
        targ_top = SCREEN_HEIGHT // 2 - targ_top
        targ_left = min(0, targ_left)
        targ_left = max(SCREEN_WIDTH - self.state.width, targ_left)
        targ_top = max(SCREEN_HEIGHT - self.state.height, targ_top)
        targ_top = min(0, targ_top)
        self.state = Rect(targ_left, targ_top, cam_width, cam_height)


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((WALL_LENGTH, WALL_LENGTH))
        self.image.fill(Color(WALL_COLOR))
        self.rect = Rect(x, y, WALL_LENGTH, WALL_LENGTH)