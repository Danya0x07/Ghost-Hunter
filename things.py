from pygame import Surface
from pygame.sprite import Sprite

from math import atan, sin, cos, sqrt


class Thing(Sprite):

    def __init__(self, size, color, **kwargs):
        super().__init__()
        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(**kwargs)

    @staticmethod
    def check_collision(object_rect, obstacles):
        for obstacle in obstacles:
            if object_rect.colliderect(obstacle):
                return obstacle

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
    def get_distance(rect_1, rect_2):
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


class MovingThing(Thing):

    def __init__(self, size, color, x_vel=0, y_vel=0, **kwargs):
        super().__init__(size, color, **kwargs)
        self.x_vel = x_vel
        self.y_vel = y_vel

    @staticmethod
    def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
        if x_vel > 0:   object_rect.right = obstacle_rect.left
        elif x_vel < 0: object_rect.left = obstacle_rect.right
        if y_vel > 0:   object_rect.bottom = obstacle_rect.top
        elif y_vel < 0: object_rect.top = obstacle_rect.bottom
