from pygame.sprite import spritecollideany

from random import randint, choice

from things import MovingThing
from plasma import EnemyPlasma, BossEnemyPlasma
from interface import Label
from config import *


class Enemy(MovingThing):
    SIZE = ENEMY_SIZE
    COLOR = ENEMY_COLOR
    FRAME_SIZE = ENEMY_FRAME_SIZE
    VEER_TIMEOUT = ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = ENEMY_SHOOT_TIMEOUT
    SPEED = ENEMY_SPEED
    HP = ENEMY_HP_MAX
    PLASMA_TYPE = EnemyPlasma

    def __init__(self, x, y):
        super().__init__(self.SIZE, self.COLOR, y_vel=1, topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=self.FRAME_SIZE, center=self.rect.center)
        self.veer_timer = Enemy.EventTimer(self.veer)
        self.veer_timeout = 120
        self.shoot_timer = Enemy.EventTimer(self.shoot)
        self.hp = self.HP
        self.lbl_hp = Label(ENEMY_HP_MAX, 16, bottomleft=self.frame_rect.bottomleft)
        self.lbl_hp_showing_timer = self.TimeoutTimer(self.draw_hp, ENEMY_HP_SHOWING_TIMEOUT)
        self.is_alive = True

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 0:
            self.is_alive = False
        self.lbl_hp_showing_timer.restart(ENEMY_HP_SHOWING_TIMEOUT)

    def draw_hp(self, scene):
        self.lbl_hp.set_text("{}%".format(self.hp), topleft=self.rect.bottomleft)
        scene.screen.blit(self.lbl_hp.image, scene.camera.apply(self.lbl_hp))

    def update(self, scene):
        self.frame_rect.x += self.x_vel
        self.collide(scene.walls, self.x_vel, 0)
        self.frame_rect.y += self.y_vel
        self.collide(scene.walls, 0, self.y_vel)
        self.rect.center = self.frame_rect.center
        self.veer_timer.update(self.veer_timeout)
        self.shoot_timer.update(self.SHOOT_TIMEOUT, (scene.player.rect, scene.plasmas))
        if not self.is_alive:
            scene.player.score += 1
            scene.enemies.remove(self)

    def change_direction(self, x_vel, y_vel):
        if x_vel != 0:
            self.x_vel = 0
            self.y_vel = choice((-self.SPEED, self.SPEED))
        elif y_vel != 0:
            self.y_vel = 0
            self.x_vel = choice((-self.SPEED, self.SPEED))

    def collide(self, walls, x_vel, y_vel):
        wall = spritecollideany(self, walls, lambda s1, s2: s1.frame_rect.colliderect(s2.rect))
        if wall is not None:
            self.handle_collision(self.frame_rect, wall.rect, x_vel, y_vel)
            self.change_direction(x_vel, y_vel)

    def veer(self):
        self.change_direction(self.x_vel, self.y_vel)
        self.veer_timeout = randint(*self.VEER_TIMEOUT)

    def shoot(self, tgt_rect, plasmas):
        if self.calc_distance(self.rect, tgt_rect) <= ENEMY_MIN_SHOOT_DISTANCE:
            x_vel, y_vel = self._shoot(self.rect, tgt_rect.center, ENEMY_PLASMA_SPEED)
            plasmas.add(self.PLASMA_TYPE(x_vel, y_vel, self.rect.center))

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(*pos))


class BossEnemy(Enemy):
    SIZE = BOSS_ENEMY_SIZE
    COLOR = BOSS_ENEMY_COLOR
    FRAME_SIZE = BOSS_ENEMY_FRAME_SIZE
    VEER_TIMEOUT = BOSS_ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = BOSS_ENEMY_SHOOT_TIMEOUT
    SPEED = BOSS_ENEMY_SPEED
    HP = BOSS_ENEMY_HP_MAX
    PLASMA_TYPE = BossEnemyPlasma
