from pygame.sprite import Sprite
from pyganim import getImagesFromSpriteSheet

from config import *


class Sofa(Sprite):
    TEXTURE_FILE = 'resources/sofa.png'
    SHEET_CONF = (3, 1)
    SIZE = (100, 50)
    POS_WORSE = (0, 50)
    POS_WORST = (0, 100)
    images = getImagesFromSpriteSheet(TEXTURE_FILE, *SIZE, *SHEET_CONF,
        [(0, 0, *SIZE), (*POS_WORSE, *SIZE), (*POS_WORST, *SIZE)])

    def __init__(self, x, y):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = FURNITURE_HP

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 33:
            self.image = self.images[2]
            return
        if self.hp <= 66:
            self.image = self.images[1]
            return

    def update(self, scene):
        if self.hp <= 0:
            scene.furniture.remove(self)


class Flower(Sofa):
    TEXTURE_FILE = 'resources/flower.png'
    SHEET_CONF = (1, 3)
    SIZE = (50, 50)
    POS_WORSE = (50, 0)
    POS_WORST = (100, 0)
    images = getImagesFromSpriteSheet(TEXTURE_FILE, *SIZE, *SHEET_CONF,
        [(0, 0, *SIZE), (*POS_WORSE, *SIZE), (*POS_WORST, *SIZE)])
