from pygame.sprite import Sprite, collide_rect, spritecollideany
from pygame import image

from random import randint

from config import *


class Plasma(Sprite):
    TEXTURE_FILE = 'resources/gplasma.png'
    OFFSET = ENEMY_PLASMA_OFFSET

    def __init__(self, x_vel, y_vel, center):
        super().__init__()
        self.image = image.load(self.TEXTURE_FILE)
        self.rect = self.image.get_rect(center=center)
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                scene.plasmas.remove(self)
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)


class BossPlasma(Plasma):
    TEXTURE_FILE = 'resources/bgplasma.png'
    OFFSET = BOSS_ENEMY_PLASMA_OFFSET


class PlayerPlasma(Plasma):
    TEXTURE_FILE = 'resources/pplasma.png'
    OFFSET = PLAYER_PLASMA_OFFSET

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                scene.plasmas.remove(self)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(self.OFFSET[1])
            scene.plasmas.remove(self)
