from pygame.sprite import collide_rect

from random import randint, choice

from things import Thing
from config import *


class HealthPoint(Thing):
    TEXTURE_FILE = 'heal.png'

    def __init__(self, position):
        super().__init__(self.TEXTURE_FILE, topleft=position)

    def update(self, scene):
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*HEALTHPOINT_OFFSET_RANGE))
            self.rect.topleft = choice(scene.hp_positions)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(pos))
