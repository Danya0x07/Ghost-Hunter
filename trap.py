from pygame.sprite import collide_rect

from things import Thing
from config import *


class Trap(Thing):

    def __init__(self, center):
        super().__init__(BOMB_SIZE, BOMB_COLOR, center=center)
        self.timeout = 0

    def update(self, enemies, healers, bombs, player):
        if self.timeout < BOMB_TIMEOUT:
            self.timeout += 1
            return
        for enemy in enemies:
            if collide_rect(self, enemy):
                player.score += 1
                enemies.remove(enemy)
        for healer in healers:
            if collide_rect(self, healer):
                healers.remove(healer)
