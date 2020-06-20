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

from collections import deque

from pygame.sprite import Sprite

from objects.pools import PoolableObject
from utils.assets import sofa_images, flower_images, furniture_breaking_sound
from utils.config import *


furniture_images = {
    'sofa': sofa_images,
    'flower': flower_images,
}


class Furniture(Sprite, PoolableObject):
    """Мебель."""
    pool = deque()

    def __init__(self, kind, x, y):
        super().__init__()
        self.kind = kind
        self.reset()
        self.rect = self.image.get_rect(topleft=(x, y))

    def shift_hp(self, offset):
        """Измененить значение здоровья на offset."""
        self.hp += offset
        if self.hp <= 33:
            self.image = furniture_images[self.kind][2]
            return
        if self.hp <= 66:
            self.image = furniture_images[self.kind][1]

    def update(self, scene):
        if self.hp <= self.next_sounding_hp:
            furniture_breaking_sound.play()
            self.next_sounding_hp -= 33
        if self.hp <= 0:
            self.delete(scene.furniture)

    def reset(self, *args):
        self.image = furniture_images[self.kind][0]
        self.hp = FURNITURE_HP
        self.next_sounding_hp = 66
