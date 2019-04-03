from pygame.sprite import collide_rect, spritecollideany, Sprite
from pygame.mixer import Sound
from pyganim import getImagesFromSpriteSheet

from util import EventTimer
from config import *


teleport_sound = Sound('resources/teleport.wav')


class Teleport(Sprite):
    images = getImagesFromSpriteSheet('resources/teleport.png', *TELEPORT_SIZE, 1, 4,
        [(0, 0, *TELEPORT_SIZE), (TELEPORT_WIDTH, 0, *TELEPORT_SIZE),
         (TELEPORT_WIDTH * 2, 0, *TELEPORT_SIZE), (TELEPORT_WIDTH * 3, 0, *TELEPORT_SIZE)])

    def __init__(self, x, y, id, tgt_id):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id = id
        self.tgt_id = tgt_id
        self.active = True
        self.current_anim_id = 0
        self.anim_timer = EventTimer(self.change_anim)

    def change_anim(self):
        self.current_anim_id += 1
        if self.current_anim_id > 3:
            self.current_anim_id = 0
        self.image = self.images[self.current_anim_id]

    def update(self, scene):
        if self.active and self.tgt_id:
            tgt_teleport = self.get_tp_by_id(scene.teleports, self.tgt_id)
            if collide_rect(self, scene.player):
                teleport_sound.play()
                scene.player.rect.center = tgt_teleport.rect.center
                tgt_teleport.active = False
            enemy = spritecollideany(self, scene.enemies)
            if enemy:
                teleport_sound.play()
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
