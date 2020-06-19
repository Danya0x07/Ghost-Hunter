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

from pygame.sprite import Sprite, spritecollideany

from objects.plasma import PlayerPlasma
from utils.util import handle_collision
from utils.ultimate_animation import UltimateAnimation
from utils.timers import RegularTimer
from utils.assets import trap_images, plasm_anim
from utils.config import *


class Trap(Sprite):
    """Капкан для привидений."""

    images = trap_images

    def __init__(self, center):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
        self.anim_timer = RegularTimer(self.change_img, TRAP_ANIM_TIMEOUT)

    def change_img(self):
        """Мигание."""
        if self.image == self.images[1]:
            self.image = self.images[0]
        else:
            self.image = self.images[1]

    def update(self, scene):
        self.anim_timer.update(scene.delta_time)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(TRAP_OFFSET)
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            handle_collision(enemy.frame_rect, self.rect, enemy.x_vel, enemy.y_vel)
            enemy.change_direction(enemy.x_vel)
        plasm = spritecollideany(self, scene.plasmas)
        if plasm is not None and type(plasm) != PlayerPlasma:
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            scene.plasmas.remove(plasm)
