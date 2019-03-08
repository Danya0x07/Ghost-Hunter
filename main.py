# -*- coding: utf-8 -*-
from pygame import init, display, quit as quit_game

from scenes import MainScene, Menu
from settings import *


def init_game():
    init()
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display.set_caption("Ghost&Hunter")
    return screen


if __name__ == '__main__':
    screen = init_game()
    menu = Menu(screen)
    game = MainScene(screen)
    while True:
        event_code = menu.mainloop()
        if event_code == 'exit':
            quit_game()
            break
        elif event_code == 'newgame':
            game = MainScene(screen)
            game.mainloop()
        elif event_code == 'continue':
            game.mainloop()