from pygame import *

if __name__ == '__main__':
    init()
    screen = display.set_mode((640, 480))
    timer = time.Clock()

    while True:
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
        timer.tick(60)
        display.update()