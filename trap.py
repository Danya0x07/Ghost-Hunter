from things import Thing
from config import *


class Trap(Thing):

    def __init__(self, center):
        super().__init__(BOMB_SIZE, BOMB_COLOR, center=center)
        self.timeout = 0

    def update(self, scene):
        if self.timeout < BOMB_TIMEOUT:
            self.timeout += 1
            return
        enemy = self.check_collision(self.rect, scene.enemies)
        if enemy:
            scene.player.score += 1
            scene.enemies.remove(enemy)
        healer = self.check_collision(self.rect, scene.healers)
        if healer:
            scene.healers.remove(healer)
