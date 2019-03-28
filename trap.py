from things import Thing
from config import *


class Trap(Thing):

    def __init__(self, center):
        super().__init__(TRAP_SIZE, TRAP_COLOR, center=center)

    def update(self, scene):
        enemy = self.check_collision(self.rect, scene.enemies)
        if enemy:
            enemy.handle_collision(enemy.frame_rect, self.rect, enemy.x_vel, enemy.y_vel)
            enemy.change_direction(enemy.x_vel, enemy.y_vel)
