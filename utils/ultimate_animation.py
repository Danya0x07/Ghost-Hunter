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

from pygame.sprite import Sprite

from utils.timers import RegularTimer


class UltimateAnimation(Sprite):
    """Конечная анимация."""""
    MAX_INDEX = 3

    def __init__(self, group, images, position, lifetime, timeout):
        super().__init__(group)
        self.images = images
        self.current_im_index = 0
        self.image = images[0]
        self.rect = self.image.get_rect(center=position)
        self.timer = RegularTimer(self._update_img, timeout)
        self.lifetime = lifetime

    def _update_img(self):
        self.image = self.images[self.current_im_index]
        self.current_im_index += 1
        if self.current_im_index > self.MAX_INDEX:
            self.current_im_index = 0

    def update(self, scene):
        self.timer.update(scene.delta_time)
        self.lifetime -= 1
        if self.lifetime <= 0:
            scene.animations.remove(self)
