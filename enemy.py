from pygame.sprite import Sprite, spritecollideany
from pygame import Surface
from spritesheet import SpriteSheet

from random import randint, choice

from things import Thing, MovingThing
from plasma import EnemyPlasma, BossEnemyPlasma
from interface import Label
from config import *


class Enemy(Sprite):
    TEXTURE_FILE = 'resources/ghost.png'
    SIZE = ENEMY_SIZE
    FRAME_SIZE = ENEMY_FRAME_SIZE
    VEER_TIMEOUT = ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = ENEMY_SHOOT_TIMEOUT
    SPEED = ENEMY_SPEED
    HP = ENEMY_HP_MAX
    PLASMA_TYPE = EnemyPlasma

    def __init__(self, x, y):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 1
        sheet = SpriteSheet(self.TEXTURE_FILE, 4, 1)
        self.img_front = Surface(self.SIZE)
        self.img_back = Surface(self.SIZE)
        self.img_left = Surface(self.SIZE)
        self.img_right = Surface(self.SIZE)
        sheet.blit(self.img_front, 0, (0, 0))
        sheet.blit(self.img_left, 1, (0, 0))
        sheet.blit(self.img_back, 2, (0, 0))
        sheet.blit(self.img_right, 3, (0, 0))
        self.img_front.set_colorkey((0, 0, 0))
        self.img_back.set_colorkey((0, 0, 0))
        self.img_left.set_colorkey((0, 0, 0))
        self.img_right.set_colorkey((0, 0, 0))
        self.image = self.img_front
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=self.FRAME_SIZE, center=self.rect.center)
        self.veer_timer = Thing.EventTimer(self.veer)
        self.veer_timeout = 120
        self.shoot_timer = Thing.EventTimer(self.shoot)
        self.hp = self.HP
        self.lbl_hp = Label(ENEMY_HP_MAX, 16, bottomleft=self.frame_rect.bottomleft)
        self.lbl_hp_showing_timer = Thing.TimeoutTimer(self.draw_hp, ENEMY_HP_SHOWING_TIMEOUT)
        self.is_alive = True

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 0:
            self.is_alive = False
        self.lbl_hp_showing_timer.restart(ENEMY_HP_SHOWING_TIMEOUT)

    def draw_hp(self, scene):
        self.lbl_hp.set_text("{}%".format(self.hp), topleft=self.rect.bottomleft)
        scene.screen.blit(self.lbl_hp.image, scene.camera.apply(self.lbl_hp))

    def refresh_img(self):
        if self.x_vel > 0:
            self.image = self.img_right
        elif self.x_vel < 0:
            self.image = self.img_left
        if self.y_vel > 0:
            self.image = self.img_back
        elif self.y_vel < 0:
            self.image = self.img_front

    def update(self, scene):
        self.frame_rect.x += self.x_vel
        self.collide(scene, self.x_vel, 0)
        self.frame_rect.y += self.y_vel
        self.collide(scene, 0, self.y_vel)
        self.rect.center = self.frame_rect.center
        self.veer_timer.update(self.veer_timeout)
        self.shoot_timer.update(self.SHOOT_TIMEOUT, (scene.player.rect, scene.plasmas))
        self.refresh_img()
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

    def collide(self, scene, x_vel, y_vel):
        for wall in scene.walls:
            if self.frame_rect.colliderect(wall):
                MovingThing.handle_collision(self.frame_rect, wall, x_vel, y_vel)
                self.change_direction(x_vel, y_vel)
        furn = spritecollideany(self, scene.furniture, lambda s1, s2: s1.frame_rect.colliderect(s2.rect))
        if furn is not None:
            MovingThing.handle_collision(self.frame_rect, furn.rect, x_vel, y_vel)
            self.change_direction(x_vel, y_vel)

    def veer(self):
        self.change_direction(self.x_vel, self.y_vel)
        self.veer_timeout = randint(*self.VEER_TIMEOUT)

    def shoot(self, tgt_rect, plasmas):
        if Thing.calc_distance(self.rect, tgt_rect) <= ENEMY_MIN_SHOOT_DISTANCE:
            x_vel, y_vel = Thing._shoot(self.rect, tgt_rect.center, ENEMY_PLASMA_SPEED)
            plasmas.add(self.PLASMA_TYPE(x_vel, y_vel, self.rect.center))

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(*pos))


class BossEnemy(Enemy):
    TEXTURE_FILE = 'resources/bossghost.png'
    SIZE = BOSS_ENEMY_SIZE
    FRAME_SIZE = BOSS_ENEMY_FRAME_SIZE
    VEER_TIMEOUT = BOSS_ENEMY_VEER_TIMEOUT
    SHOOT_TIMEOUT = BOSS_ENEMY_SHOOT_TIMEOUT
    SPEED = BOSS_ENEMY_SPEED
    HP = BOSS_ENEMY_HP_MAX
    PLASMA_TYPE = BossEnemyPlasma
