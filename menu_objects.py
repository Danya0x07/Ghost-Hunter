from pygame import Surface, Rect
from pygame.sprite import Sprite
from pygame.font import Font

from config import *


class Button(Sprite):

    def __init__(self, text, id, position, size=BTN_SIZE, active=True):
        super().__init__()
        self.text = text
        self.__id = id
        self.active = active
        self.font = Font('resources/freesansbold.ttf', BTN_FONT_SIZE)
        self.txt_color = BTN_TXT_USUAL_COLOR
        self.txt_image = self.font.render(text, True, self.txt_color, BTN_BG_COLOR)
        self.txt_rect = self.txt_image.get_rect()
        self.txt_rect.center = (BTN_WIDTH // 2, BTN_HEIGHT // 2)

        self.tile_image = Surface(BTN_SIZE)
        self.tile_image.fill(BTN_BG_COLOR)
        self.tile_rect = Rect(position, size)

    def check_pressed(self, position):
        return self.active and self.tile_rect.collidepoint(*position)

    def refresh_txt_img(self, txt_color):
        if self.txt_color != txt_color:
            self.txt_color = txt_color
            self.txt_image = self.font.render(self.text, True, txt_color, BTN_BG_COLOR)

    def update(self, position):
        if not self.active:
            self.refresh_txt_img(BTN_TXT_INACTIVE_COLOR)
            return
        if self.tile_rect.collidepoint(*position):
            self.refresh_txt_img(BTN_TXT_SELECTED_COLOR)
        else:
            self.refresh_txt_img(BTN_TXT_USUAL_COLOR)

    def draw(self, surface):
        self.tile_image.blit(self.txt_image, self.txt_rect)
        surface.blit(self.tile_image, self.tile_rect)

    @property
    def id(self):
        return self.__id

    @staticmethod
    def get_btn_pos(frame, position):
        return frame.left, frame.top + position * BTN_HEIGHT


class Label(Sprite):

    def __init__(self, text, fontsize=LBL_FONT_SIZE, color=LBL_TXT_COLOR):
        super().__init__()
        self.font = Font('resources/freesansbold.ttf', fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()

    def set_text(self, text, color=LBL_TXT_COLOR):
        self.image = self.font.render(text, True, color)
