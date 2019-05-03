# -*- coding: utf-8 -*-
from pygame import init, display, quit as quit_game
from pygame.locals import FULLSCREEN
init()
from scenes import MainScene, Menu, GameOverScene
from config import *

import sys


def init_game():
    screen = display.set_mode(SCREEN_SIZE, FULLSCREEN)
    display.set_caption("Haunted Library")
    return screen


if __name__ == '__main__':
    if sys.platform == 'win32':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    screen = init_game()
    menu = Menu(screen)
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
                menu = Menu(screen)
