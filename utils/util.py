from math import atan, sin, cos, sqrt


def shoot(src_pos, tgt_pos, plasm_spd):
    """Получить вектор скорости для попадания из src_pos в tgt_pos."""
    dx = tgt_pos[0] - src_pos[0]
    dy = tgt_pos[1] - src_pos[1]
    if dx == 0:
        x_vel = 0
        y_vel = plasm_spd if dy > 0 else -plasm_spd
    else:
        angle = atan(dy / dx)
        x_vel = cos(angle) * plasm_spd
        y_vel = sin(angle) * plasm_spd
        if tgt_pos[0] < src_pos[0]:
            x_vel = -x_vel
            y_vel = -y_vel
    return x_vel, y_vel


def calc_distance(rect_1, rect_2):
    """Вычислить расстояние между двумя прямоугольниками."""
    dx = rect_1.centerx - rect_2.centerx
    dy = rect_1.centery - rect_2.centery
    distance = int(sqrt(dx ** 2 + dy ** 2))
    return distance


def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
    """
    Обработать столкновение объекта с препятствием,
    не дать пройти насквозь.
    """
    if x_vel > 0:   object_rect.right = obstacle_rect.left
    elif x_vel < 0: object_rect.left = obstacle_rect.right
    if y_vel > 0:   object_rect.bottom = obstacle_rect.top
    elif y_vel < 0: object_rect.top = obstacle_rect.bottom


class EventTimer:
    """Таймер регулярного повторения."""

    def __init__(self, handler):
        self.handler = handler
        self.counter = 0

    def update(self, timeout, args=()):
        if self.counter >= timeout:
            self.counter = 0
            self.handler(*args)
        else: self.counter += 1


class CountdownTimer:
    """Таймер обратного отсчёта."""

    def __init__(self, handler, timeout):
        self.handler = handler
        self.counter = timeout

    def update(self, *args):
        if self.counter > 0:
            self.handler(*args)
            self.counter -= 1

    def restart(self, new_timeout):
        self.counter = new_timeout


class UltimateAnimation:
    """Конечная анимация."""""
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

    def draw(self, scene):
        scene.screen.blit(self.image, scene.camera.apply(self.rect))
        self.timer.update(self.timeout * scene.delta_time)
        self.lifetime -= 1
        if self.lifetime <= 0:
            scene.animations.remove(self)
