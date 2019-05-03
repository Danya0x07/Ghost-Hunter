from math import atan, sin, cos, sqrt


def shoot(rel_rect, tgt_pos, plasm_spd):
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


def calc_distance(rect_1, rect_2):
    dx = rect_1.centerx - rect_2.centerx
    dy = rect_1.centery - rect_2.centery
    distance = int(sqrt(dx ** 2 + dy ** 2))
    return distance


def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
    if x_vel > 0:   object_rect.right = obstacle_rect.left
    elif x_vel < 0: object_rect.left = obstacle_rect.right
    if y_vel > 0:   object_rect.bottom = obstacle_rect.top
    elif y_vel < 0: object_rect.top = obstacle_rect.bottom


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


class Animation:
    MAX_INDEX = 3

    def __init__(self, images, position, lifetime, timeout):
        self.images = images
        self.current_im_index = 0
        self.image = images[0]
        self.rect = self.image.get_rect(center=position)
        self.timer = EventTimer(self.update_img)
        self.lifetime = lifetime
        self.timeout = timeout

    def update_img(self):
        self.image = self.images[self.current_im_index]
        self.current_im_index += 1
        if self.current_im_index > self.MAX_INDEX:
            self.current_im_index = 0

    def update(self, surface, camera):
        surface.blit(self.image, camera.apply(self))
        self.timer.update(self.timeout)
        self.lifetime -= 1
