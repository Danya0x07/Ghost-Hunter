from pygame.sprite import Sprite, collide_rect
from pygame import image
from pygame.mixer import Sound

from random import randint, choice

from config import *


heal_sound = Sound('resources/heal.wav')


class HealthPoint(Sprite):
    image = image.load('resources/heal.png')

    def __init__(self, position):
        super().__init__()
        self.rect = self.image.get_rect(topleft=position)

    def update(self, scene):
        if collide_rect(self, scene.player):
            heal_sound.play()
            scene.player.shift_hp(randint(*HEALTHPOINT_OFFSET_RANGE))
            self.rect.topleft = choice(scene.hp_positions)

    @classmethod
    def random_spawn(cls, positions, group, number=1):
        for i in range(number):
            pos = choice(positions)
            group.add(cls(pos))
