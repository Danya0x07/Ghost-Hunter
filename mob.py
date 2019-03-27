from random import randint, choice
from math import sqrt

from things import MovingThing
from plasma import Plasma, EnemyPlasma, HealerPlasma
from config import *


class Mob(MovingThing):
    SIZE = (50, 50)
    COLOR = (0, 0, 0)
    FRAME_SIZE = (70, 70)
    VEER_TIMEOUT = (120, 180)
    SHOOT_TIMEOUT = 30
    SPEED = 5
    BULLET_TYPE = Plasma

    def __init__(self, x, y):
        super().__init__(self.SIZE, self.COLOR, y_vel=1, topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=self.FRAME_SIZE, center=self.rect.center)
        self.veer_timer = Mob.EventTimer(self.veer)
        self.veer_timeout = 120
        self.shoot_timer = Mob.EventTimer(self.shoot)

    def update(self, scene):
        self.frame_rect.x += self.x_vel
        self.collide(scene.walls, self.x_vel, 0)
        self.frame_rect.y += self.y_vel
        self.collide(scene.walls, 0, self.y_vel)
        self.rect.center = self.frame_rect.center
        self.veer_timer.update(self.veer_timeout)
        self.shoot_timer.update(self.SHOOT_TIMEOUT, (scene.plasmas,))

    def change_direction(self, x_vel, y_vel):
        if x_vel != 0:
            self.x_vel = 0
            self.y_vel = choice((-self.SPEED, self.SPEED))
        elif y_vel != 0:
            self.y_vel = 0
            self.x_vel = choice((-self.SPEED, self.SPEED))

    def collide(self, walls, x_vel, y_vel):
        wall = self.check_collision(self.frame_rect, walls)
        if wall is not None:
            self.handle_collision(self.frame_rect, wall.rect, x_vel, y_vel)
            self.change_direction(x_vel, y_vel)

    def veer(self):
        self.change_direction(self.x_vel, self.y_vel)
        self.veer_timeout = randint(*self.VEER_TIMEOUT)

    def shoot(self, plasmas):
        x_vel = randint(-self.BULLET_TYPE.SPEED, self.BULLET_TYPE.SPEED)
        y_vel = int(sqrt(self.BULLET_TYPE.SPEED ** 2 - x_vel ** 2)) * choice((-1, 1))
        plasma = self.BULLET_TYPE(x_vel, y_vel, self.rect.center)
        plasmas.add(plasma)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(*pos))

    class EventTimer:

        def __init__(self, handler):
            self.handler = handler
            self.counter = 0

        def update(self, timeout, args=()):
            if self.counter >= timeout:
                self.counter = 0
                self.handler(*args)
            else: self.counter += 1


class Enemy(Mob):
    SIZE = ENEMY_SIZE
    COLOR = ENEMY_COLOR
    FRAME_SIZE = ENEMY_FRAME_SIZE
    VEER_TIMEOUT = ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = ENEMY_SHOOT_TIMEOUT
    SPEED = ENEMY_SPEED
    BULLET_TYPE = EnemyPlasma


class Healer(Mob):
    SIZE = HEALER_SIZE
    COLOR = HEALER_COLOR
    FRAME_SIZE = HEALER_FRAME_SIZE
    VEER_TIMEOUT = HEALER_VEER_TIMEOUT
    SHOOT_TIMEOUT = HEALER_SHOOT_TIMEOUT
    SPEED = HEALER_SPEED
    BULLET_TYPE = HealerPlasma
