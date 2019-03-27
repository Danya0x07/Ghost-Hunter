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

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        if self.check_collision(self.rect, scene.walls):
            scene.plasmas.remove(self)
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)


class EnemyPlasma(Plasma):
    SIZE = DAMAGE_PLASMA_SIZE
    COLOR = DAMAGE_PLASMA_COLOR
    SPEED = DAMAGE_PLASMA_SPEED
    OFFSET = DAMAGE_PLASMA_OFFSET


class HealerPlasma(Plasma):
    SIZE = HEAL_PLASMA_SIZE
    COLOR = HEAL_PLASMA_COLOR
    SPEED = HEAL_PLASMA_SPEED
    OFFSET = HEAL_PLASMA_OFFSET


class PlayerPlasma(MovingThing):
    SIZE = PLAYER_PLASMA_SIZE
    COLOR = PLAYER_PLASMA_COLOR
    SPEED = PLAYER_PLASMA_SPEED
    OFFSET = PLAYER_PLASMA_OFFSET

    def __init__(self, x_vel, y_vel, center):
        super().__init__(self.SIZE, self.COLOR, x_vel, y_vel, center=center)

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        if self.check_collision(self.rect, scene.walls):
            scene.plasmas.remove(self)
        enemy = self.check_collision(self.rect, scene.enemies)
        if enemy:
            scene.enemies.remove(enemy)
            scene.player.score += 1
        healer = self.check_collision(self.rect, scene.healers)
        if healer:
            scene.healers.remove(healer)
