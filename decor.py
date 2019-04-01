from pygame.sprite import Sprite
from pygame import Surface
from spritesheet import SpriteSheet

from things import Thing
from config import *


class Wall(Thing):

    def __init__(self, x, y):
        super().__init__(WALL_SIZE, WALL_COLOR, topleft=(x, y))


class Sofa(Sprite):
    TEXTURE_FILE = 'resources/sofa.png'
    SHEET_CONF = (1, 3)
    SIZE = (100, 50)
    POS_WORSE = (0, 50)
    POS_WORST = (0, 100)

    def __init__(self, x, y):
        super().__init__()
        sheet = SpriteSheet(self.TEXTURE_FILE, *self.SHEET_CONF)
        self.img_normal = Surface(self.SIZE)
        self.img_worse = Surface(self.SIZE)
        self.img_worst = Surface(self.SIZE)
        sheet.blit(self.img_normal, 0, (0, 0))
        sheet.blit(self.img_worse, 1, (0, 0))
        sheet.blit(self.img_worst, 2, (0, 0))
        self.img_normal.set_colorkey((0, 0, 0))
        self.img_worse.set_colorkey((0, 0, 0))
        self.img_worst.set_colorkey((0, 0, 0))
        self.image = self.img_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = FURNITURE_HP

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 33:
            self.image = self.img_worst
            return
        if self.hp <= 66:
            self.image = self.img_worse
            return

    def update(self, scene):
        if self.hp <= 0:
            scene.furniture.remove(self)


class Flower(Sofa):
    TEXTURE_FILE = 'resources/flower.png'
    SHEET_CONF = (3, 1)
    SIZE = (50, 50)
    POS_WORSE = (50, 0)
    POS_WORST = (100, 0)
