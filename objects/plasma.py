from pygame.sprite import Sprite, collide_rect, spritecollideany

from random import randint

from utils.util import Animation
from utils.assets import (plasm_anim, player_plasma_image,
                          enemy_plasma_image, boss_enemy_plasma_image)
from utils.config import *


class Plasma(Sprite):
    image = enemy_plasma_image
    offset = ENEMY_PLASMA_OFFSET

    def __init__(self, x_vel, y_vel, center):
        super().__init__()
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
            furn.shift_hp(randint(*self.offset))
            scene.animations.append(Animation(plasm_anim, self.rect.center, 9, 3))
            scene.plasmas.remove(self)
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*self.offset))
            scene.animations.append(Animation(plasm_anim, self.rect.center, 9, 3))
            scene.plasmas.remove(self)


class BossPlasma(Plasma):
    image = boss_enemy_plasma_image
    offset = BOSS_ENEMY_PLASMA_OFFSET


class PlayerPlasma(Plasma):
    image = player_plasma_image
    offset = PLAYER_PLASMA_OFFSET

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                scene.plasmas.remove(self)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(randint(*self.offset))
            scene.animations.append(Animation(plasm_anim, self.rect.center, 9, 3))
            scene.plasmas.remove(self)
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(self.offset[1])
            scene.animations.append(Animation(plasm_anim, self.rect.center, 9, 3))
            scene.plasmas.remove(self)
