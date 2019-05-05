from pygame.sprite import Sprite, spritecollideany

from utils.util import handle_collision
from utils.ultimate_animation import UltimateAnimation
from utils.timers import EventTimer
from utils.assets import trap_images, plasm_anim
from utils.config import *


class Trap(Sprite):
    """Капкан для привидений."""

    images = trap_images

    def __init__(self, center):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=center)
        self.anim_timer = EventTimer(self.change_img, TRAP_ANIM_TIMEOUT)

    def change_img(self):
        """Мигание."""
        if self.image == self.images[1]:
            self.image = self.images[0]
        else:
            self.image = self.images[1]

    def update(self, scene):
        self.anim_timer.update(scene.delta_time)
        enemy = spritecollideany(self, scene.enemies)
        if enemy:
            enemy.shift_hp(TRAP_OFFSET)
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            handle_collision(enemy.frame_rect, self.rect, enemy.x_vel, enemy.y_vel)
            enemy.change_direction(enemy.x_vel)
        plasm = spritecollideany(self, scene.plasmas)
        if plasm:
            UltimateAnimation(scene.animations, plasm_anim, self.rect.center, 9, 3)
            scene.plasmas.remove(plasm)
