from pygame.sprite import collide_rect
from pygame.locals import *


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
        self.pk_level = 0
        self.pkl_timer = self.EventTimer(self.refresh_pkl)

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

    def update(self, scene):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -PLAYER_SPEED
        if back:  self.y_vel = PLAYER_SPEED
        if left:  self.x_vel = -PLAYER_SPEED
        if right: self.x_vel = PLAYER_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += self.x_vel
        self.collide(scene.walls, self.x_vel, 0)
        self.rect.y += self.y_vel
        self.collide(scene.walls, 0, self.y_vel)
        self.pkl_timer.update(PKL_UPDATE_TIMEOUT, (scene.enemies,))

    def collide(self, walls, x_vel, y_vel):
        wall = self.check_collision(self.rect, walls)
        if wall is not None:
            self.handle_collision(self.rect, wall.rect, x_vel, y_vel)

    def handle_trap(self, traps, wave):
        for trap in traps:
            if collide_rect(self, trap):
                traps.remove(trap)
                return
        if len(traps) <= wave:
            trap = Trap(self.rect.center)
            traps.add(trap)

    def refresh_pkl(self, enemies):
        min_distance = SCREEN_WIDTH * SCREEN_HEIGHT
        for enemy in enemies:
            distance = self.get_distance(self.rect, enemy.rect)
            if distance < min_distance:
                min_distance = distance
        self.pk_level =  100 - min(min_distance * 100 // PKL_MAX_DISTANCE, 100)


    def shoot(self, rel_rect, m_pos, plasmas):
        x_vel, y_vel = MovingThing._shoot(rel_rect, m_pos, PLAYER_PLASMA_SPEED)
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
