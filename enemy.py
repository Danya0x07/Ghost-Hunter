from random import randint, choice
from math import sqrt

from things import MovingThing
from plasma import EnemyPlasma
from config import *


class Enemy(MovingThing):
    SIZE = ENEMY_SIZE
    COLOR = ENEMY_COLOR
    FRAME_SIZE = ENEMY_FRAME_SIZE
    VEER_TIMEOUT = ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = ENEMY_SHOOT_TIMEOUT
    SPEED = ENEMY_SPEED

    def __init__(self, x, y):
        super().__init__(self.SIZE, self.COLOR, y_vel=1, topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=self.FRAME_SIZE, center=self.rect.center)
        self.veer_timer = Enemy.EventTimer(self.veer)
        self.veer_timeout = 120
        self.shoot_timer = Enemy.EventTimer(self.shoot)

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
        x_vel = randint(-ENEMY_PLASMA_SPEED, ENEMY_PLASMA_SPEED)
        y_vel = int(sqrt(ENEMY_PLASMA_SPEED ** 2 - x_vel ** 2)) * choice((-1, 1))
        plasma = EnemyPlasma(x_vel, y_vel, self.rect.center)
        plasmas.add(plasma)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(*pos))
