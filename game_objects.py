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


class Thing(Sprite):

    def __init__(self, size, color, **kwargs):
        super().__init__()
        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(**kwargs)


class MovingThing(Thing):

    def __init__(self, size, color, x_vel=0, y_vel=0, **kwargs):
        super().__init__(size, color, **kwargs)
        self.x_vel = x_vel
        self.y_vel = y_vel

    @staticmethod
    def check_collision(object_rect, obstacles):
        for obstacle in obstacles:
            if object_rect.colliderect(obstacle):
                return obstacle

    @staticmethod
    def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
        if x_vel > 0:   object_rect.right = obstacle_rect.left
        elif x_vel < 0: object_rect.left = obstacle_rect.right
        if y_vel > 0:   object_rect.bottom = obstacle_rect.top
        elif y_vel < 0: object_rect.top = obstacle_rect.bottom


class Player(MovingThing):

    def __init__(self, x, y):
        super().__init__(PLAYER_SIZE, PLAYER_COLOR, topleft=(x, y))
        self.dir = Direction()
        self.hp = PLAYER_HP_MAX
        self.score = 0
        self.is_alive = True

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp > PLAYER_HP_MAX:
            self.hp = PLAYER_HP_MAX
        elif self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            self.is_alive = False

    def set_direction(self, key, state):
        if key == K_w:   self.dir.front = state
        elif key == K_s: self.dir.back = state
        elif key == K_a: self.dir.left = state
        elif key == K_d: self.dir.right = state

    def update(self, walls):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -PLAYER_SPEED
        if back:  self.y_vel = PLAYER_SPEED
        if left:  self.x_vel = -PLAYER_SPEED
        if right: self.x_vel = PLAYER_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += self.x_vel
        self.collide(walls, self.x_vel, 0)
        self.rect.y += self.y_vel
        self.collide(walls, 0, self.y_vel)

    def collide(self, walls, x_vel, y_vel):
        wall = self.check_collision(self.rect, walls)
        if wall is not None:
            self.handle_collision(self.rect, wall.rect, x_vel, y_vel)

    def lay_bomb(self, bombs):
        bomb = Bomb(self.rect.center)
        bombs.add(bomb)


class Enemy(MovingThing):

    def __init__(self, x, y):
        super().__init__(ENEMY_SIZE, ENEMY_COLOR, y_vel=1, topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=ENEMY_FRAME_SIZE, center=self.rect.center)
        self.veer_counter = 0
        self.veer_time = 120
        self.shoot_counter = 0

    def handle_shooting(self, plasmas):
        if self.shoot_counter >= ENEMY_SHOOT_TIMEOUT:
            self.shoot(plasmas)
            self.shoot_counter = 0
        else:
            self.shoot_counter += 1

    def handle_veering(self):
        if self.veer_counter >= self.veer_time:
            self.change_direction(self.x_vel, self.y_vel)
            self.veer_counter = 0
            self.veer_time = randint(*ENEMY_VEER_TIMEOUT)
        else:
            self.veer_counter += 1

    def update(self, walls, plasmas):
        self.frame_rect.x += self.x_vel
        self.collide(walls, self.x_vel, 0)
        self.frame_rect.y += self.y_vel
        self.collide(walls, 0, self.y_vel)
        self.rect.center = self.frame_rect.center
        self.handle_shooting(plasmas)
        self.handle_veering()

    def change_direction(self, x_vel, y_vel):
        if x_vel != 0:
            self.x_vel = 0
            self.y_vel = choice((-ENEMY_SPEED, ENEMY_SPEED))
        elif y_vel != 0:
            self.y_vel = 0
            self.x_vel = choice((-ENEMY_SPEED, ENEMY_SPEED))

    def collide(self, walls, x_vel, y_vel):
        wall = self.check_collision(self.frame_rect, walls)
        if wall is not None:
            self.handle_collision(self.frame_rect, wall.rect, x_vel, y_vel)
            self.change_direction(x_vel, y_vel)

    def shoot(self, plasmas):
        x_vel = randint(-PLASMA_SPEED, PLASMA_SPEED)
        y_vel = int(sqrt(PLASMA_SPEED ** 2 - x_vel ** 2)) * choice((-1, 1))
        plasma = Plasma(x_vel, y_vel, self.rect.center)
        plasmas.add(plasma)


class Wall(Thing):

    def __init__(self, x, y):
        super().__init__(WALL_SIZE, WALL_COLOR, topleft=(x, y))


class Plasma(MovingThing):

    def __init__(self, x_vel, y_vel, center):
        super().__init__(PLASMA_SIZE, PLASMA_COLOR, x_vel, y_vel, center=center)
        self.damage = randint(*PLASMA_DAMAGE)

    def update(self, walls, plasmas, player):
        self.rect.move_ip(self.x_vel, self.y_vel)
        self.collide(walls, plasmas, player)

    def collide(self, walls, plasmas, player):
        if self.check_collision(self.rect, walls):
            plasmas.remove(self)
        if collide_rect(self, player):
            player.shift_hp(-self.damage)
            plasmas.remove(self)


class Bomb(Thing):

    def __init__(self, center):
        super().__init__(BOMB_SIZE, BOMB_COLOR, center=center)
        self.timeout = 0

    def update(self, enemies, bombs, player):
        if self.timeout < BOMB_TIMEOUT:
            self.timeout += 1
        for enemy in enemies:
            if collide_rect(self, enemy):
                player.score += 1
                enemies.remove(enemy)
                bombs.remove(self)
        if collide_rect(self, player) and self.timeout >= BOMB_TIMEOUT:
            player.shift_hp(-PLAYER_HP_MAX)
            bombs.remove(self)


class Camera:

    def __init__(self, level_size):
        width, height = level_size
        self.state = Rect(0, 0, width, height)

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
