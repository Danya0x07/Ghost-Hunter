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

"""Игра про охоту на привидений.

Шутер от 3 лица, вид сверху.
Задача: уничтожить как можно больше привидений.
"""

import sys

from pygame import init as pg_init, display, quit as pg_quit
from pygame.locals import FULLSCREEN

pg_init()  # Next imports require videosystem being initialized.

from scenes.main_scene import MainScene
from scenes.menu_scene import MenuScene
from scenes.gamover_scene import GameOverScene
from utils.config import *


__author__ = "Daniel Efimenko"
__copyright__ = "Copyright 2019, The Haunted_Library project"
__credits__ = ["Daniel Efimenko", "Alexander Isaev", "Maxim Babenko"]
__license__ = "GPL"
__version__ = "1.2.0"
__maintainer__ = "Daniel Efimenko"
__email__ = "dlef0xf8@gmail.com"
__status__ = "Production"


def init_game():
    screen = display.set_mode(SCREEN_SIZE, FULLSCREEN)
    display.set_caption("Haunted Library")
    return screen


if __name__ == '__main__':
    if sys.platform == 'win32':
        try:  # На древних машинах не находит schore, а разрешение и так норм.
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except FileNotFoundError:
            pass
            
    screen = init_game()
    menu = MenuScene(screen)
    game = MainScene(screen)
    end = GameOverScene(screen)
    
    while True:
        event_code = menu.mainloop()
        if event_code == 'exit':
            pg_quit()
            break
        else:
            if event_code == 'newgame':
                game.restart()
                event_code = game.mainloop()
            elif event_code == 'continue':
                event_code = game.mainloop()
            if event_code == 'gameover':
                end.set_stats(game.stats)
                end.mainloop()
                menu.restart()
