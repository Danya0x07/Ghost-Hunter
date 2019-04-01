from pygame import image, Surface
from pygame.sprite import Sprite

from math import atan, sin, cos, sqrt


class Thing(Sprite):

    def __init__(self, filename, **kwargs):
        super().__init__()
        self.image = image.load('resources/{}'.format(filename))
        self.rect = self.image.get_rect(**kwargs)

    @staticmethod
    def _shoot(rel_rect, tgt_pos, plasm_spd):
        dx = tgt_pos[0] - rel_rect.centerx
        dy = tgt_pos[1] - rel_rect.centery
        if dx == 0:
            x_vel = 0
            y_vel = plasm_spd if dy > 0 else -plasm_spd
        else:
            angle = atan(dy / dx)
            x_vel = int(cos(angle) * plasm_spd)
            y_vel = int(sin(angle) * plasm_spd)
            if tgt_pos[0] < rel_rect.centerx:
                x_vel = -x_vel
                y_vel = -y_vel
        return x_vel, y_vel

    @staticmethod
    def calc_distance(rect_1, rect_2):
        dx = rect_1.centerx - rect_2.centerx
        dy = rect_1.centery - rect_2.centery
        distance = int(sqrt(dx ** 2 + dy ** 2))
        return distance

    class EventTimer:

        def __init__(self, handler):
            self.handler = handler
            self.counter = 0

        def update(self, timeout, args=()):
            if self.counter >= timeout:
                self.counter = 0
                self.handler(*args)
            else: self.counter += 1

    class TimeoutTimer:

        def __init__(self, handler, counter):
            self.handler = handler
            self.counter = counter

        def update(self, *args):
            if self.counter > 0:
                self.handler(*args)
                self.counter -= 1

        def restart(self, counter):
            self.counter = counter


class MovingThing(Thing):

    def __init__(self, filename, x_vel=0, y_vel=0, **kwargs):
        super().__init__(filename, **kwargs)
        self.x_vel = x_vel
        self.y_vel = y_vel

    @staticmethod
    def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
        if x_vel > 0:   object_rect.right = obstacle_rect.left
        elif x_vel < 0: object_rect.left = obstacle_rect.right
        if y_vel > 0:   object_rect.bottom = obstacle_rect.top
        elif y_vel < 0: object_rect.top = obstacle_rect.bottom
