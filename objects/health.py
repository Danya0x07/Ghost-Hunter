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

from pygame.sprite import Sprite, collide_rect

from utils.assets import heal_image, heal_sound
from utils.config import *


class HealthPoint(Sprite):
    """Заряд позитива."""
    image = heal_image

    def __init__(self, position):
        super().__init__()
        self.rect = self.image.get_rect(topleft=position)

    def update(self, scene):
        if collide_rect(self, scene.player):
            heal_sound.play()
            scene.player.shift_hp(randint(*HEALTHPOINT_OFFSET_RANGE))
            self.rect.topleft = choice(scene.hp_spawn_positions)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        """Создать множество объектов в случайных местах"""
        for i in range(number):
            pos = choice(positions)
            group.add(cls(pos))
