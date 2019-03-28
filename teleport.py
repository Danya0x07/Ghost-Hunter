from pygame.sprite import collide_rect, spritecollideany

from things import Thing
from config import *


class Teleport(Thing):

    def __init__(self, x, y, id, tgt_id):
        super().__init__(TELEPORT_SIZE, TELEPORT_COLOR, topleft=(x, y))
        self.id = id
        self.tgt_id = tgt_id
        self.active = True

    def update(self, scene):
        if self.active and self.tgt_id:
            tgt_teleport = self.get_tp_by_id(scene.teleports, self.tgt_id)
            if collide_rect(self, scene.player):
                scene.player.rect.center = tgt_teleport.rect.center
                tgt_teleport.active = False
            enemy = spritecollideany(self, scene.enemies)
            if enemy:
                enemy.frame_rect.center = tgt_teleport.rect.center
                tgt_teleport.active = False
        else:
            is_overlayed = False
            if collide_rect(self, scene.player):
                is_overlayed = True
            if spritecollideany(self, scene.enemies, lambda s1, s2: s1.rect.colliderect(s2.frame_rect)):
                is_overlayed = True
            self.active = not is_overlayed

    @staticmethod
    def get_tp_by_id(group, id):
        for tp in group:
            if tp.id == id:
                return tp
