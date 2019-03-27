from pygame.sprite import collide_rect
from pygame.locals import *

from math import atan, sin, cos

from things import MovingThing
from trap import Trap
from plasma import PlayerPlasma
from config import *


class Player(MovingThing):

    def __init__(self, x, y):
        super().__init__(PLAYER_SIZE, PLAYER_COLOR, topleft=(x, y))
        self.dir = Player.Direction()
        self.hp = PLAYER_HP_MAX
        self.score = 0
        self.is_alive = True
        self.available_traps = 1

    def shift_hp(self, offset):
        self.hp += offset
        if self.hp > PLAYER_HP_MAX:
            self.hp = PLAYER_HP_MAX
        elif self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            self.is_alive = False

    def set_direction(self, key, state):
        if key == K_w:   self.dir.front = state
        elif key == K_s: self.dir.back = state
        elif key == K_a: self.dir.left = state
        elif key == K_d: self.dir.right = state

    def update(self, walls):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -PLAYER_SPEED
        if back:  self.y_vel = PLAYER_SPEED
        if left:  self.x_vel = -PLAYER_SPEED
        if right: self.x_vel = PLAYER_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += self.x_vel
        self.collide(walls, self.x_vel, 0)
        self.rect.y += self.y_vel
        self.collide(walls, 0, self.y_vel)

    def collide(self, walls, x_vel, y_vel):
        wall = self.check_collision(self.rect, walls)
        if wall is not None:
            self.handle_collision(self.rect, wall.rect, x_vel, y_vel)

    def handle_trap(self, traps, limit):
        for trap in traps:
            if collide_rect(self, trap):
                traps.remove(trap)
                return
        if len(traps) < limit:
            trap = Trap(self.rect.center)
            traps.add(trap)

    def shoot(self, m_pos, pl_rect, plasmas):
        dx = m_pos[0] - pl_rect.centerx
        dy = m_pos[1] - pl_rect.centery
        if dx == 0:
            x_vel = 0
            y_vel = PLAYER_PLASMA_SPEED if dy > 0 else -PLAYER_PLASMA_SPEED
        else:
            angle = atan(dy / dx)
            x_vel = int(cos(angle) * PLAYER_PLASMA_SPEED)
            y_vel = int(sin(angle) * PLAYER_PLASMA_SPEED)
            if m_pos[0] < pl_rect.centerx:
                x_vel = -x_vel
                y_vel = -y_vel
        plasmas.add(PlayerPlasma(x_vel, y_vel, self.rect.center))

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
