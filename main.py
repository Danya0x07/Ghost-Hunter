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
    game = MainScene(screen)
    menu = Menu(screen)
    while True:
        event_code = menu.mainloop()
        if event_code == 'exit':
            quit_game()
            break
        elif event_code == 'play':
            game.mainloop()