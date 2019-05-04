from pygame.sprite import Sprite, spritecollideany
from pygame.locals import *

from objects.trap import Trap
from objects.plasma import PlayerPlasma
from utils.util import EventTimer, handle_collision, calc_distance, shoot
from utils.assets import (player_images, player_walk_sound, player_shoot_sound,
                          player_auch_sound, trap_down_sound, trap_up_sound)
from utils.config import *


class Player(Sprite):
    images = player_images

    def __init__(self, x, y):
        super().__init__()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.walk_sound_playing = False
        self.dir = Player.Direction()
        self.x_vel = 0
        self.y_vel = 0
        self.hp = PLAYER_HP_MAX
        self.score = 0
        self.is_alive = True
        self.pk_level = 0
        self.pkl_timer = EventTimer(self.refresh_pkl)

    def shift_hp(self, offset):
        if offset < 0:
            player_auch_sound.play()
        self.hp += offset
        if self.hp > PLAYER_HP_MAX:
            self.hp = PLAYER_HP_MAX
        elif self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            self.is_alive = False
            player_walk_sound.stop()

    def set_direction(self, key, state):
        img_num = None
        if key == K_w:
            self.dir.front = state
            img_num = 0
        elif key == K_s:
            self.dir.back = state
            img_num = 2
        elif key == K_a:
            self.dir.left = state
            img_num = 1
        elif key == K_d:
            self.dir.right = state
            img_num = 3
        if state and img_num is not None:
            self.image = self.images[img_num]
            if not self.walk_sound_playing:
                player_walk_sound.play(-1)
                self.walk_sound_playing = True

    def update(self, scene):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -PLAYER_SPEED
        if back:  self.y_vel = PLAYER_SPEED
        if left:  self.x_vel = -PLAYER_SPEED
        if right: self.x_vel = PLAYER_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += int(self.x_vel * scene.delta_time)
        self.collide(scene, self.x_vel, 0)
        self.rect.y += int(self.y_vel * scene.delta_time)
        self.collide(scene, 0, self.y_vel)
        self.pkl_timer.update(PKL_UPDATE_TIMEOUT * scene.delta_time, (scene.enemies,))
        if self.x_vel == 0 and self.y_vel == 0:
            player_walk_sound.stop()
            self.walk_sound_playing = False

    def collide(self, scene, x_vel, y_vel):
        for wall in scene.walls:
            if self.rect.colliderect(wall):
                handle_collision(self.rect, wall, x_vel, y_vel)
        furn = spritecollideany(self, scene.furniture)
        if furn is not None:
            handle_collision(self.rect, furn.rect, x_vel, y_vel)

    def handle_trap(self, traps, wave):
        trap = spritecollideany(self, traps)
        if trap is not None:
            trap_up_sound.play()
            traps.remove(trap)
            return
        if len(traps) <= wave:
            trap_down_sound.play()
            trap = Trap(self.rect.center)
            traps.add(trap)

    def refresh_pkl(self, enemies):
        min_distance = SCREEN_WIDTH * SCREEN_HEIGHT
        for enemy in enemies:
            distance = calc_distance(self.rect, enemy.rect)
            if distance < min_distance:
                min_distance = distance
        self.pk_level =  100 - min(min_distance * 100 // PKL_MAX_DISTANCE, 100)


    def shoot(self, rel_rect, m_pos, plasmas, delta):
        x_vel, y_vel = shoot(rel_rect, m_pos, PLAYER_PLASMA_SPEED)
        plasmas.add(PlayerPlasma(x_vel, y_vel, self.rect.center))
        player_shoot_sound.play()

    class Direction:

        def __init__(self):
            self.front = False
            self.back = False
            self.left = False
            self.right = False

        def set_dir_state(self, front, back, left, right):
            self.front = front
            self.back = back
            self.left = left
            self.right = right

        def get_dir_state(self):
            return self.front, self.back, self.left, self.right
