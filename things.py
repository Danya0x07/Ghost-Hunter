from pygame import Surface
from pygame.sprite import Sprite


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
