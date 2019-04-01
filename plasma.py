from pygame.sprite import collide_rect, spritecollideany

from random import randint

from things import MovingThing
from config import *


class EnemyPlasma(MovingThing):
    SIZE = ENEMY_PLASMA_SIZE
    COLOR = ENEMY_PLASMA_COLOR
    OFFSET = ENEMY_PLASMA_OFFSET

    def __init__(self, x_vel, y_vel, center):
        super().__init__(self.SIZE, self.COLOR, x_vel, y_vel, center=center)

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                scene.plasmas.remove(self)
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)
        if collide_rect(self, scene.player):
            scene.player.shift_hp(randint(*self.OFFSET))
            scene.plasmas.remove(self)


class BossEnemyPlasma(EnemyPlasma):
    SIZE = BOSS_ENEMY_PLASMA_SIZE
    COLOR = BOSS_ENEMY_PLASMA_COLOR
    OFFSET = BOSS_ENEMY_PLASMA_OFFSET


class PlayerPlasma(MovingThing):
    SIZE = PLAYER_PLASMA_SIZE
    COLOR = PLAYER_PLASMA_COLOR
    OFFSET = PLAYER_PLASMA_OFFSET

    def __init__(self, x_vel, y_vel, center):
        super().__init__(self.SIZE, self.COLOR, x_vel, y_vel, center=center)

    def update(self, scene):
        self.rect.move_ip(self.x_vel, self.y_vel)
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                scene.plasmas.remove(self)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(-self.OFFSET)
            scene.plasmas.remove(self)
        furn = spritecollideany(self, scene.furniture)
        if furn:
            furn.shift_hp(-self.OFFSET)
            scene.plasmas.remove(self)
