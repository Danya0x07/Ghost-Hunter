# Copyright (C) 2019-2020, Daniel Efimenko
#
# This file is part of Haunted_Library.
#
# Haunted_Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Haunted_Library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Haunted_Library.  If not, see <https://www.gnu.org/licenses/>.
#

from random import randint
from collections import deque

from pygame.sprite import Sprite, collide_rect, spritecollideany

from objects.pools import PoolableObject
from utils.ultimate_animation import UltimateAnimation
from utils.assets import (plasm_anim, player_plasma_image,
                          enemy_plasma_image, boss_enemy_plasma_image)
from utils.config import *


class Plasma(Sprite, PoolableObject):
    """Базовый класс для плазмы. Плазма привидений."""

    image = enemy_plasma_image
    offset = ENEMY_PLASMA_OFFSET
    pool = deque()

    def __init__(self, x_vel, y_vel, center):
        super().__init__()
        self.reset(x_vel, y_vel, center)

    def move(self, scene):
        self.rect.x += round(self.x_vel * scene.delta_time)
        self.rect.y += round(self.y_vel * scene.delta_time)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                self.delete(scene.plasmas)
                break

    def handle_collision_with_furniture(self, scene):
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(self.offset[1])
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            self.delete(scene.plasmas)

    def update(self, scene):
        self.move(scene)
        self.handle_collision_with_furniture(scene)
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*self.offset))
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            self.delete(scene.plasmas)

    def reset(self, x_vel, y_vel, center):
        self.rect = self.image.get_rect(center=center)
        self.x_vel = x_vel
        self.y_vel = y_vel


class BossPlasma(Plasma):
    """Плазма привидений-боссов."""

    image = boss_enemy_plasma_image
    offset = BOSS_ENEMY_PLASMA_OFFSET
    pool = deque()


class PlayerPlasma(Plasma, PoolableObject):
    """Плазма игрока."""

    image = player_plasma_image
    offset = PLAYER_PLASMA_OFFSET
    pool = deque()

    def update(self, scene):
        self.move(scene)
        self.handle_collision_with_furniture(scene)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(randint(*self.offset))
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            self.delete(scene.plasmas)
