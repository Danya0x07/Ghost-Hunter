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

from pygame import event, mouse
from pygame.locals import *

from scenes.scene import Scene
from utils.interface import Button, Label
from utils.config import *


class GameOverScene(Scene):
    """Сцена поражения."""

    def __init__(self, screen):
        super().__init__(screen, MENU_BG_COLOR)
        self.stats = None
        self.btn_back = Button("to menu", 'tomenu',
                               rectsize=(150, 60), fontsize=24, bottomleft=(0, SCREEN_HEIGHT))
        self.lbl_gameover = Label("Game Over!", 70, midbottom=self.screen_rect.center)

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == MOUSEBUTTONDOWN:
                if self.btn_back.check_pressed(mouse.get_pos()):
                    self.return_code = self.btn_back.id

    def update_objects(self):
        self.btn_back.update(mouse.get_pos())

    def set_stats(self, stats):
        self.stats = stats

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.screen.blit(self.lbl_gameover.image, self.lbl_gameover.rect)
        self.btn_back.draw(self.screen)
        self.stats.draw(self.screen)
