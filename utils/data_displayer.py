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

from pygame.sprite import Group

from utils.interface import Label


class DataDisplayer:
    """Визуализатор данных игры."""

    class SmartLabel(Label):
        """Экономно обновляющаяся текстовая метка."""

        def __init__(self, text, fontsize, param=None):
            super().__init__(text, fontsize)
            self.text = text
            self.param = param

        def update(self, *param, **kwargs):
            if self.param != param:
                self.param = param
                self.set_text(self.text.format(*param), **kwargs)


    def __init__(self):
        self.lbl_hp = DataDisplayer.SmartLabel("Mood: {}%", 30)
        self.lbl_score = DataDisplayer.SmartLabel("Score: {}", 30)
        self.lbl_wave = DataDisplayer.SmartLabel("Wave: {}", 35)
        self.lbl_enemies = DataDisplayer.SmartLabel("Ghosts: {}/{}", 30)
        self.lbl_traps = DataDisplayer.SmartLabel("Traps: {}/{}", 30)
        self.lbl_pkl = DataDisplayer.SmartLabel("PK level: {}%", 25)
        self.labels = Group(
            self.lbl_hp,
            self.lbl_score,
            self.lbl_wave,
            self.lbl_enemies,
            self.lbl_traps,
            self.lbl_pkl
        )

    def update(self, scene):
        self.lbl_hp.update(scene.player.hp, topleft=scene.screen_rect.topleft)
        self.lbl_score.update(scene.player.score, topleft=self.lbl_hp.rect.bottomleft)
        self.lbl_wave.update(scene.wave, centerx=scene.screen_rect.centerx)
        self.lbl_enemies.update(scene.wave - len(scene.enemies), scene.wave,
                                topright=scene.screen_rect.topright)
        self.lbl_traps.update(scene.wave + 1 - len(scene.traps), scene.wave + 1,
                                topright=self.lbl_enemies.rect.bottomright)
        self.lbl_pkl.update(scene.player.pk_level, bottomright=scene.screen_rect.bottomright)

    def draw(self, surface):
        self.labels.draw(surface)
