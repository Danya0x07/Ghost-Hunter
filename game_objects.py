from pygame import Surface, Rect
from pygame.sprite import Sprite, collide_rect
from pygame.locals import *

from random import choice, randint
from math import sqrt

from config import *


class Direction:

    def __init__(self):
        self.front = False
        self.back = False
        self.left = False
        self.right = False

    def set_dir_state(self, front, back, left, right):
        self.front = front
        self.back = back
        self.left = left
        self.right = right

    def get_dir_state(self):
        return self.front, self.back, self.left, self.right


class Hunter(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.x_vel = 0
        self.y_vel = 0
        self.dir = Direction()
        self.image = Surface(HUNTER_SIZE)
        self.image.fill(HUNTER_COLOR)
        self.rect = Rect((x, y), HUNTER_SIZE)

    def set_direction(self, key, state):
        if key == K_w:   self.dir.front = state
        elif key == K_s: self.dir.back = state
        elif key == K_a: self.dir.left = state
        elif key == K_d: self.dir.right = state

    def update(self, walls):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -HUNTER_SPEED
        if back:  self.y_vel = HUNTER_SPEED
        if left:  self.x_vel = -HUNTER_SPEED
        if right: self.x_vel = HUNTER_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += self.x_vel
        self.check_collision(walls, self.x_vel, 0)
        self.rect.y += self.y_vel
        self.check_collision(walls, 0, self.y_vel)

    def check_collision(self, walls, x_vel, y_vel):
        for wall in walls:
            if collide_rect(self, wall):
                if x_vel > 0:   self.rect.right = wall.rect.left
                elif x_vel < 0: self.rect.left = wall.rect.right
                if y_vel > 0:   self.rect.bottom = wall.rect.top
                elif y_vel < 0: self.rect.top = wall.rect.bottom


class Enemy(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.x_vel = 0
        self.y_vel = -ENEMY_SPEED
        self.dir = Direction()
        self.image = Surface(ENEMY_SIZE)
        self.image.fill(ENEMY_COLOR)
        self.rect = Rect((x, y), ENEMY_SIZE)
        self.frame_rect = Rect((0, 0), ENEMY_FRAME_SIZE)
        self.frame_rect.center = self.rect.center
        self.shoot_counter = 0
        self.move_counter = 0
        self.move_time = 120

    def update(self, walls, plasmas):
        self.frame_rect.x += self.x_vel
        self.check_collision(walls, self.x_vel, 0)
        self.frame_rect.y += self.y_vel
        self.check_collision(walls, 0, self.y_vel)
        self.rect.center = self.frame_rect.center

        if self.shoot_counter >= ENEMY_SHOOT_TIME:
            self.shoot(plasmas)
            self.shoot_counter = 0
        else: self.shoot_counter += 1

        if self.move_counter >= self.move_time:
            self.move_counter = 0
            self.move_time = randint(60, 180)
            self.change_direction(self.x_vel, self.y_vel)
        else: self.move_counter += 1

    def change_direction(self, x_vel, y_vel):
        if x_vel != 0:
            self.x_vel = 0
            self.y_vel = choice((-ENEMY_SPEED, ENEMY_SPEED))
        elif y_vel != 0:
            self.y_vel = 0
            self.x_vel = choice((-ENEMY_SPEED, ENEMY_SPEED))

    def check_collision(self, walls, x_vel, y_vel):
        for wall in walls:
            if self.frame_rect.colliderect(wall):
                if x_vel > 0:   self.frame_rect.right = wall.rect.left
                elif x_vel < 0: self.frame_rect.left = wall.rect.right
                if y_vel > 0:   self.frame_rect.bottom = wall.rect.top
                elif y_vel < 0: self.frame_rect.top = wall.rect.bottom
                self.change_direction(x_vel, y_vel)

    def shoot(self, plasmas):
        x_vel = randint(-PLASMA_SPEED, PLASMA_SPEED)
        y_vel = int(sqrt(PLASMA_SPEED ** 2 - x_vel ** 2)) * choice((-1, 1))
        plasma = Plasma(x_vel, y_vel, self.rect.center)
        plasmas.add(plasma)


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = Surface(WALL_SIZE)
        self.image.fill(WALL_COLOR)
        self.rect = Rect((x, y), WALL_SIZE)


class Plasma(Sprite):

    def __init__(self, x_vel, y_vel, center):
        super().__init__()
        self.image = Surface(PLASMA_SIZE)
        self.image.fill(PLASMA_COLOR)
        self.rect = self.image.get_rect(center=center)
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self, walls, plasmas):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.check_collision(walls, plasmas)

    def check_collision(self, walls, plasmas):
        for wall in walls:
            if collide_rect(self, wall):
                plasmas.remove(self)


class Camera:

    def __init__(self, level_width, level_height):
        self.state = Rect(0, 0, level_width, level_height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        tg_left, tg_top, tg_width, tg_height = target.rect
        cam_left, cam_top, cam_width, cam_height = self.state
        tg_left = SCREEN_WIDTH // 2 - tg_left
        tg_top = SCREEN_HEIGHT // 2 - tg_top
        tg_left = min(0, tg_left)
        tg_left = max(SCREEN_WIDTH - self.state.width, tg_left)
        tg_top = max(SCREEN_HEIGHT - self.state.height, tg_top)
        tg_top = min(0, tg_top)
        self.state = Rect(tg_left, tg_top, cam_width, cam_height)
