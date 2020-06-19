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

from random import randint, choice
from collections import deque

from pygame.sprite import Sprite, spritecollideany

from objects.plasma import Plasma, BossPlasma
from objects.pools import PoolableObject
from utils.util import calc_distance, handle_collision, shoot
from utils.timers import RegularTimer, CountdownTimer
from utils.ultimate_animation import UltimateAnimation
from utils.interface import Label
from utils.assets import (enemy_images, boss_enemy_images, enemy_dying_anim,
                          enemy_shoot_sound, enemy_auch_sound)
from utils.config import *


class Enemy(Sprite, PoolableObject):
    """Привидение"""

    frame_size = ENEMY_FRAME_SIZE
    veer_timeout = ENEMY_VEER_TIMEOUT
    shoot_timeout = ENEMY_SHOOT_TIMEOUT
    speed = ENEMY_SPEED
    hp = ENEMY_HP_MAX
    PlasmaType = Plasma
    kill_award = 1
    images = enemy_images
    pool = deque()

    def __init__(self, x, y):
        super().__init__()
        self.reset(x, y)
        self.veer_timer = RegularTimer(self.veer, self.veer_timeout[0])
        self.shoot_timer = RegularTimer(self.shoot, self.shoot_timeout)
        self.lbl_hp = Label(ENEMY_HP_MAX, 16, bottomleft=self.frame_rect.bottomleft)
        self.lbl_hp_showing_timer = CountdownTimer(self._draw_hp, ENEMY_HP_SHOWING_TIMEOUT)

    def update(self, scene):
        self.frame_rect.x += int(self.x_vel * scene.delta_time)
        self.collide(scene, self.x_vel, 0)
        self.frame_rect.y += int(self.y_vel * scene.delta_time)
        self.collide(scene, 0, self.y_vel)
        self.rect.center = self.frame_rect.center
        self.veer_timer.update(scene.delta_time)
        self.shoot_timer.update(scene.delta_time, (scene.player.rect, scene.plasmas))
        if not self.is_alive:
            scene.player.score += self.kill_award
            UltimateAnimation(scene.animations, enemy_dying_anim, self.rect.center, 30, 10)
            self.delete(scene.enemies)

    def shift_hp(self, offset):
        """Измененить значение здоровья на offset."""
        if offset < 0:
            enemy_auch_sound.play()
        self.hp += offset
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
        self.lbl_hp_showing_timer.restart(ENEMY_HP_SHOWING_TIMEOUT)

    def _draw_hp(self, screen, camera):
        """Отрисовать значение здоровья."""
        self.lbl_hp.set_text("{}%".format(self.hp), topleft=self.rect.bottomleft)
        screen.blit(self.lbl_hp.image, camera.apply(self.lbl_hp.rect))

    def draw_hp_if_need(self, scene):
        """Обёртка для таймера отрисовки здоровья."""
        self.lbl_hp_showing_timer.update(scene.delta_time, (scene.screen, scene.camera))

    def refresh_img(self):
        """Обновить текстуру при повороте."""
        if self.x_vel > 0:
            self.image = self.images[3]
        elif self.x_vel < 0:
            self.image = self.images[1]
        if self.y_vel > 0:
            self.image = self.images[2]
        elif self.y_vel < 0:
            self.image = self.images[0]

    def change_direction(self, x_vel):
        """Изменить направление движения."""
        if x_vel != 0:
            self.x_vel = 0
            self.y_vel = choice((-self.speed, self.speed))
        else:
            self.y_vel = 0
            self.x_vel = choice((-self.speed, self.speed))
        self.refresh_img()

    def collide(self, scene, x_vel, y_vel):
        """Проверка на столкновение с объектами."""
        for wall in scene.walls:
            if self.frame_rect.colliderect(wall):
                handle_collision(self.frame_rect, wall, x_vel, y_vel)
                self.change_direction(x_vel)
        furn = spritecollideany(self, scene.furniture, lambda s1, s2: s1.frame_rect.colliderect(s2.rect))
        if furn is not None:
            handle_collision(self.frame_rect, furn.rect, x_vel, y_vel)
            self.change_direction(x_vel)

    def veer(self):
        """Обёртка для таймера блуждания"""
        self.change_direction(self.x_vel)
        self.veer_timer.timeout = randint(*self.veer_timeout)

    def shoot(self, tgt_rect, plasmas):
        """Стрельба."""
        if calc_distance(self.rect, tgt_rect) <= ENEMY_MAX_SHOOT_DISTANCE:
            enemy_shoot_sound.play()
            x_vel, y_vel = shoot(self.rect.center, tgt_rect.center, ENEMY_PLASMA_SPEED)
            plasmas.add(self.PlasmaType.create(x_vel, y_vel, self.rect.center))

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        """Создать множество объектов в случайных местах"""
        for i in range(number):
            pos = choice(positions)
            group.add(cls.create(*pos))

    def reset(self, x, y):
        self.x_vel = 0
        self.y_vel = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rect = self.image.get_rect(size=self.frame_size, center=self.rect.center)
        self.is_alive = True


class BossEnemy(Enemy, PoolableObject):
    """Привидение-босс"""

    frame_size = BOSS_ENEMY_FRAME_SIZE
    veer_timeout = BOSS_ENEMY_VEER_TIMEOUT
    shoot_timeout = BOSS_ENEMY_SHOOT_TIMEOUT
    speed = BOSS_ENEMY_SPEED
    hp = BOSS_ENEMY_HP_MAX
    PlasmaType = BossPlasma
    kill_award = 3
    images = boss_enemy_images
    pool = deque()
