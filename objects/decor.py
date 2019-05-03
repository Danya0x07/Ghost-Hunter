from pygame.sprite import Sprite

from utils.animages import sofa_images, flower_images
from utils.sounds import furniture_breaking_sound
from utils.config import *


class Sofa(Sprite):
    images = sofa_images

    def __init__(self, x, y):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = FURNITURE_HP
        self.next_sounding_hp = 66

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 33:
            self.image = self.images[2]
            return
        if self.hp <= 66:
            self.image = self.images[1]

    def update(self, scene):
        if self.hp <= self.next_sounding_hp:
            furniture_breaking_sound.play()
            self.next_sounding_hp -= 33
        if self.hp <= 0:
            scene.furniture.remove(self)


class Flower(Sofa):
    images = flower_images
