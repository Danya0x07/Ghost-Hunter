from pygame.sprite import collide_rect

from random import randint

from things import MovingThing
from config import *


class Plasma(MovingThing):
    SIZE = (16, 16)
    COLOR = (255, 255, 255)
    SPEED = 20
    OFFSET = (0, 0)

    def __init__(self, x_vel, y_vel, center):
        super().__init__(self.SIZE, self.COLOR, x_vel, y_vel, center=center)

    def update(self, walls, plasmas, player):
        self.rect.move_ip(self.x_vel, self.y_vel)
        self.collide(walls, plasmas, player)

    def collide(self, walls, plasmas, player):
        if self.check_collision(self.rect, walls):
            plasmas.remove(self)
        if collide_rect(self, player):
            player.shift_hp(randint(*self.OFFSET))
            plasmas.remove(self)


class DamagePLasma(Plasma):
    SIZE = DAMAGE_PLASMA_SIZE
    COLOR = DAMAGE_PLASMA_COLOR
    SPEED = DAMAGE_PLASMA_SPEED
    OFFSET = DAMAGE_PLASMA_OFFSET


class HealPlasma(Plasma):
    SIZE = HEAL_PLASMA_SIZE
    COLOR = HEAL_PLASMA_COLOR
    SPEED = HEAL_PLASMA_SPEED
    OFFSET = HEAL_PLASMA_OFFSET
