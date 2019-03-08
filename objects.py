from pygame import Surface, Color, Rect
from pygame.sprite import Sprite, collide_rect
from pygame.font import Font
from pygame.locals import *

from settings import *


class Direction:

    def __init__(self):
        self.front = False
        self.back = False
        self.left = False
        self.right = False

    def get_dir_state(self):
        return self.front, self.back, self.left, self.right


class Hunter(Sprite):
    WIDTH = 32
    HEIGHT = 32
    MOVE_SPEED = 5
    COLOR = "#AAAAAA"

    def __init__(self, x, y):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.x_vel = 0
        self.y_vel = 0
        self.dir = Direction()
        self.image = Surface((Hunter.WIDTH, Hunter.HEIGHT))
        self.image.fill(Color(Hunter.COLOR))
        self.rect = Rect(x, y, Hunter.WIDTH, Hunter.HEIGHT)

    def set_direction(self, key, state):
        if key == K_w:   self.dir.front = state
        elif key == K_s: self.dir.back = state
        elif key == K_a: self.dir.left = state
        elif key == K_d: self.dir.right = state

    def update(self, walls):
        front, back, left, right = self.dir.get_dir_state()
        if front: self.y_vel = -Hunter.MOVE_SPEED
        if back:  self.y_vel = Hunter.MOVE_SPEED
        if left:  self.x_vel = -Hunter.MOVE_SPEED
        if right: self.x_vel = Hunter.MOVE_SPEED
        if not (front or back): self.y_vel = 0
        if not (left or right): self.x_vel = 0
        self.rect.x += self.x_vel
        self.check_collision(walls, self.x_vel, 0)
        self.rect.y += self.y_vel
        self.check_collision(walls, 0, self.y_vel)

    def check_collision(self, walls, x_vel, y_vel):
        for wall in walls:
            if collide_rect(self, wall):
                if x_vel > 0:   self.rect.right = wall.rect.left
                elif x_vel < 0: self.rect.left = wall.rect.right
                if y_vel > 0:   self.rect.bottom = wall.rect.top
                elif y_vel < 0: self.rect.top = wall.rect.bottom


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((WALL_LENGTH, WALL_LENGTH))
        self.image.fill(Color(WALL_COLOR))
        self.rect = Rect(x, y, WALL_LENGTH, WALL_LENGTH)


class Camera:

    def __init__(self, level_width, level_height):
        self.state = Rect(0, 0, level_width, level_height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        tg_left, tg_top, tg_width, tg_height = target.rect
        cam_left, cam_top, cam_width, cam_height = self.state
        tg_left = SCREEN_WIDTH // 2 - tg_left
        tg_top = SCREEN_HEIGHT // 2 - tg_top
        tg_left = min(0, tg_left)
        tg_left = max(SCREEN_WIDTH - self.state.width, tg_left)
        tg_top = max(SCREEN_HEIGHT - self.state.height, tg_top)
        tg_top = min(0, tg_top)
        self.state = Rect(tg_left, tg_top, cam_width, cam_height)


class Button(Sprite):
    TXT_USUAL_COLOR = Color(BTN_TXT_USUAL_COLOR)
    TXT_SELECTED_COLOR = Color(BTN_TXT_SELECTED_COLOR)
    TXT_INACTIVE_COLOR = Color(BTN_TXT_INACTIVE_COLOR)
    BG_COLOR = Color(BTN_BG_COLOR)

    def __init__(self, text, id, position, size=(BTN_WIDTH, BTN_HEIGHT), active=True):
        super().__init__()
        self.text = text
        self.__id = id
        self.active = active
        self.font = Font('resources/freesansbold.ttf', BTN_FONT_SIZE)
        self.txt_color = Button.TXT_USUAL_COLOR
        self.txt_image = self.font.render(text, True, self.txt_color, Button.BG_COLOR)
        self.txt_rect = self.txt_image.get_rect()
        self.txt_rect.center = (BTN_WIDTH // 2, BTN_HEIGHT // 2)

        self.tile_image = Surface((BTN_WIDTH, BTN_HEIGHT))
        self.tile_image.fill(Button.BG_COLOR)
        self.tile_rect = Rect(position, size)

    def check_pressed(self, position):
        return self.active and self.tile_rect.collidepoint(*position)

    def refresh_txt_img(self, txt_color):
        if self.txt_color != txt_color:
            self.txt_color = txt_color
            self.txt_image = self.font.render(self.text, True, txt_color, Button.BG_COLOR)

    def update(self, position):
        if not self.active:
            self.refresh_txt_img(Button.TXT_INACTIVE_COLOR)
            return
        if self.tile_rect.collidepoint(*position):
            self.refresh_txt_img(Button.TXT_SELECTED_COLOR)
        else:
            self.refresh_txt_img(Button.TXT_USUAL_COLOR)

    def draw(self, surface):
        self.tile_image.blit(self.txt_image, self.txt_rect)
        surface.blit(self.tile_image, self.tile_rect)

    @property
    def id(self):
        return self.__id

    @staticmethod
    def get_btn_pos(frame, position):
        return frame.left, frame.top + position * BTN_HEIGHT
