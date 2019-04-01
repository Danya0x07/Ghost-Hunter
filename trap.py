from pygame.sprite import Sprite, spritecollideany
from pygame import Surface
from spritesheet import SpriteSheet

from things import Thing, MovingThing
from config import *


class Trap(Sprite):
    TEXTURE_FILE = 'resources/trap.png'

    def __init__(self, center):
        super().__init__()
        sheet = SpriteSheet(self.TEXTURE_FILE, 2, 1)
        self.img_1 = Surface(TRAP_SIZE)
        self.img_2 = Surface(TRAP_SIZE)
        sheet.blit(self.img_1, 0, (0, 0))
        sheet.blit(self.img_2, 1, (0, 0))
        self.image = self.img_1
        self.rect = self.image.get_rect(center=center)
        self.anim_timer = Thing.EventTimer(self.change_img)

    def change_img(self):
        if self.image == self.img_2:
            self.image = self.img_1
        else:
            self.image = self.img_2

    def update(self, scene):
        self.anim_timer.update(TRAP_ANIM_TIMEOUT, ())
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(TRAP_OFFSET)
            MovingThing.handle_collision(enemy.frame_rect, self.rect, enemy.x_vel, enemy.y_vel)
            enemy.change_direction(enemy.x_vel, enemy.y_vel)
