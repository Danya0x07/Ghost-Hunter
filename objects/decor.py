from pygame.sprite import Sprite

from utils.assets import sofa_images, flower_images, furniture_breaking_sound
from utils.config import *


furniture_images = {
    'sofa': sofa_images,
    'flower': flower_images,
}


class Furniture(Sprite):
    """Мебель."""

    def __init__(self, kind, x, y):
        super().__init__()
        self.kind = kind
        self.image = furniture_images[kind][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = FURNITURE_HP
        self.next_sounding_hp = 66

    def shift_hp(self, offset):
        """Измененить значение здоровья на offset."""
        self.hp += offset
        if self.hp <= 33:
            self.image = furniture_images[self.kind][2]
            return
        if self.hp <= 66:
            self.image = furniture_images[self.kind][1]

    def update(self, scene):
        if self.hp <= self.next_sounding_hp:
            furniture_breaking_sound.play()
            self.next_sounding_hp -= 33
        if self.hp <= 0:
            scene.furniture.remove(self)
