# -*- coding: utf-8 -*-
"""A game about ghost hunting.

Player is a ghostbuster in a haunted library.
Game is endless, the more ghosts player hunts down, the better
ghostbuster he is.
"""

import sys

from pygame import init, display, quit as quit_game
from pygame.locals import FULLSCREEN
init()

from scenes.main_scene import MainScene
from scenes.menu_scene import MenuScene
from scenes.gamover_scene import GameOverScene
from utils.config import *


__author__ = "Daniil Efimenko"
__copyright__ = "Copyright 2019, The Haunted_Library project"
__credits__ = ["Daniil Efimenko", "Alexander Isaev", "Maxim Babenko"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "Daniil Efimenko"
__email__ = "danya9104449383@gmail.com"
__status__ = "Production"


def init_game():
    screen = display.set_mode(SCREEN_SIZE, FULLSCREEN)
    display.set_caption("Haunted Library")
    return screen


if __name__ == '__main__':
    if sys.platform == 'win32':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    screen = init_game()
    menu = MenuScene(screen)
    game = MainScene(screen)
    while True:
        event_code = menu.mainloop()
        if event_code == 'exit':
            quit_game()
            break
        else:
            if event_code == 'newgame':
                game = MainScene(screen)
                event_code = game.mainloop()
            elif event_code == 'continue':
                event_code = game.mainloop()
            if event_code == 'gameover':
                GameOverScene(screen, game.stats).mainloop()
                menu = MenuScene(screen)
