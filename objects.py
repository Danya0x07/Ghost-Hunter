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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((WALL_LENGTH, WALL_LENGTH))
        self.image.fill(Color(WALL_COLOR))
        self.rect = Rect(x, y, WALL_LENGTH, WALL_LENGTH)


class Camera:

    def __init__(self, level):
        w, h = Camera.get_total_level_size(level)
        self.state = Rect(0, 0, w, h)

    @staticmethod
    def get_total_level_size(level):
        t_width = len(level[0]) * WALL_LENGTH
        t_height = len(level) * WALL_LENGTH
        return t_width, t_height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        targ_left, targ_top, targ_width, targ_height = target.rect
        cam_left, cam_top, cam_width, cam_height = self.state
        targ_left = SCREEN_WIDTH // 2 - targ_left
        targ_top = SCREEN_HEIGHT // 2 - targ_top
        targ_left = min(0, targ_left)
        targ_left = max(SCREEN_WIDTH - self.state.width, targ_left)
        targ_top = max(SCREEN_HEIGHT - self.state.height, targ_top)
        targ_top = min(0, targ_top)
        self.state = Rect(targ_left, targ_top, cam_width, cam_height)


class Button(Sprite):
    USUAL_COLOR = Color(BTN_USUAL_COLOR)
    SELECTED_COLOR = Color(BTN_SELECTED_COLOR)
    BG_COLOR = Color(BTN_BG_COLOR)
    BLIT_LEFT_X = SCREEN_WIDTH // 2 - BTN_WIDTH // 2


    def __init__(self, text, screen_rect):
        super().__init__()
        self.text = text
        self.font = Font('resources/freesansbold.ttf', 34)
        self.image = self.font.render(text, True, Button.USUAL_COLOR)
        self.sensetive_rect = Rect(0, 0, BTN_WIDTH, BTN_HEIGHT)
        self.sensetive_rect.center = screen_rect.center

        self.rect = self.image.get_rect()
        print(self.rect.height)
        self.surface = Surface((BTN_WIDTH, BTN_HEIGHT))
        self.surface.fill(Button.BG_COLOR)
        self.x_blit = BTN_WIDTH // 2 - self.rect.width // 2
        self.y_blit = BTN_HEIGHT // 2 - self.rect.height // 2


        self.current_color = Button.USUAL_COLOR
        self.last_color = self.current_color

    def check_pressed(self, position):
        return self.sensetive_rect.collidepoint(*position)

    def update(self, position):
        if self.sensetive_rect.collidepoint(*position):
            if self.current_color != Button.SELECTED_COLOR:
                self.current_color = Button.SELECTED_COLOR
                self.image = self.font.render(self.text, True, self.current_color, Button.BG_COLOR)
        else:
            if self.current_color != Button.USUAL_COLOR:
                self.current_color = Button.USUAL_COLOR
                self.image = self.font.render(self.text, True, self.current_color, Button.BG_COLOR)

    def draw(self, screen):
        y = SCREEN_HEIGHT // 2 - BTN_HEIGHT // 2
        self.surface.blit(self.image, (self.x_blit, self.y_blit))
        screen.blit(self.surface, (Button.BLIT_LEFT_X, y))



