from things import Thing
from config import *


class Wall(Thing):

    def __init__(self, x, y):
        super().__init__(WALL_SIZE, WALL_COLOR, topleft=(x, y))


class Furniture(Thing):

    def __init__(self, x, y):
        super().__init__(FURNITURE_SIZE, FURNITURE_USUAL_COLOR, topleft=(x, y))
        self.hp = FURNITURE_HP

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp <= 33:
            self.image.fill(FURNITURE_WORST_COLOR)
            return
        if self.hp <= 66:
            self.image.fill(FURNITURE_WORSE_COLOR)
            return

    def update(self, scene):
        if self.hp <= 0:
            scene.furniture.remove(self)
