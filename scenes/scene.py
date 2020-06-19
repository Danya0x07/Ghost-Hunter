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

from pygame import display, Surface
from pygame.time import Clock

from utils.config import *


class Scene:
    """Базовый класс для всех сцен"""

    def __init__(self, screen, bg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.space = Surface(SCREEN_SIZE)
        self.space.fill(bg)
        self.clock = Clock()
        self.return_code = None

    def check_events(self):
        """Проверить события приложения."""
        pass

    def update_objects(self):
        """Обновить объектов"""
        pass

    def draw_objects(self):
        """Отрисовать объекты."""
        pass

    def mainloop(self):
        """Главный цикл сцены."""
        self.return_code = None
        # Чтобы сбросить число, возвращаемое clock.get_time()
        self.clock.tick(FPS)
        self.clock.tick(FPS)

        while self.return_code is None:
            self.check_events()
            self.update_objects()
            self.draw_objects()
            self.clock.tick(FPS)
            display.flip()
        return self.return_code
