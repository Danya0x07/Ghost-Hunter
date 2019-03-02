from pygame import init, display

from scenes import MainScene
from settings import *


def init_game():
    init()
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display.set_caption("Ghost&Hunter")
    return screen


if __name__ == '__main__':
    screen = init_game()
    game = MainScene(screen)
    game.mainloop()