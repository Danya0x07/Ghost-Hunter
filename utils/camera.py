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

from pygame import Rect

from utils.config import *


class Camera:
    """Игровая камера, следующая за игроком."""

    def __init__(self, level_size):
        width, height = level_size
        self.state = Rect(0, 0, width, height)

    def apply(self, pos):
        """Получить относительные координаты по абсолютным."""
        return pos[0] + self.state.left, pos[1] + self.state.top

    def update(self, target):
        """Центрироваться относительно цели."""
        tg_left, tg_top, tg_width, tg_height = target.rect
        cam_left, cam_top, cam_width, cam_height = self.state
        tg_left = SCREEN_WIDTH // 2 - tg_left
        tg_top = SCREEN_HEIGHT // 2 - tg_top
        tg_left = min(0, tg_left)
        tg_left = max(SCREEN_WIDTH - self.state.width, tg_left)
        tg_top = max(SCREEN_HEIGHT - self.state.height, tg_top)
        tg_top = min(0, tg_top)
        self.state = Rect(tg_left, tg_top, cam_width, cam_height)

    def reverse(self, pos):
        """Получить абсолютные координаты по относительным."""
        return pos[0] - self.state.left, pos[1] - self.state.top
