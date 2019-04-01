from pygame.sprite import collide_rect, spritecollideany, Sprite
from pygame import Surface
from spritesheet import SpriteSheet

from things import Thing
from config import *


class Teleport(Sprite):
    TEXTURE_FILE = 'resources/teleport.png'

    def __init__(self, x, y, id, tgt_id):
        super().__init__()
        self.sheet = SpriteSheet(self.TEXTURE_FILE, 4, 1)
        self.image = Surface(TELEPORT_SIZE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id = id
        self.tgt_id = tgt_id
        self.active = True
        self.current_anim_id = 0
        self.anim_timer = Thing.EventTimer(self.change_anim)

    def change_anim(self):
        self.sheet.blit(self.image, self.current_anim_id, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.current_anim_id += 1
        if self.current_anim_id > 3:
            self.current_anim_id = 0

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
        self.anim_timer.update(TELEPORT_ANIM_TIMEOUT, ())

    @staticmethod
    def get_tp_by_id(group, id):
        for tp in group:
            if tp.id == id:
                return tp
