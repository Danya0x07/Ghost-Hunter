from objects import Hunter
from scenes import MainScene


if __name__ == '__main__':
    hunter = Hunter(0, 0)
    game = MainScene(hunter)
    game.mainloop()