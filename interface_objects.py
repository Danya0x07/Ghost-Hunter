from pygame import Surface
from pygame.sprite import Sprite, Group
from pygame.font import Font

from config import *


class Button(Sprite):

    def __init__(self, text, id, rectsize, fontsize, active=True, **kwargs):
        super().__init__()
        self.text = text
        self.__id = id
        self.active = active
        self.font = Font('resources/freesansbold.ttf', fontsize)
        self.txt_color = BTN_TXT_USUAL_COLOR
        self.txt_image = self.font.render(text, True, self.txt_color, BTN_BG_COLOR)
        self.txt_rect = self.txt_image.get_rect()
        self.txt_rect.center = (rectsize[0] // 2, rectsize[1] // 2)

        self.tile_image = Surface(rectsize)
        self.tile_image.fill(BTN_BG_COLOR)
        self.tile_rect = self.tile_image.get_rect(**kwargs)

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
    def get_btn_pos(frame, position, height):
        return frame.left, frame.top + position * height


class Label(Sprite):

    def __init__(self, text, fontsize, color=LBL_TXT_DEFAULT_COLOR, **kwargs):
        super().__init__()
        self.font = Font('resources/freesansbold.ttf', fontsize)
        self.image = self.font.render(str(text), True, color)
        self.rect = self.image.get_rect(**kwargs)

    def set_text(self, text, color=LBL_TXT_DEFAULT_COLOR, **kwargs):
        self.image = self.font.render(str(text), True, color)
        self.rect = self.image.get_rect(**kwargs)


class DataDisplayer:

    def __init__(self, player, frame):
        self.player = player
        self.frame = frame
        self.lbl_hp = Label("", 30)
        self.lbl_score = Label("", 30)
        self.lbl_wave = Label("", 35)
        self.lbl_enemies = Label("", 30)
        self.lbl_traps = Label("", 30)
        self.labels = Group(
            self.lbl_hp,
            self.lbl_score,
            self.lbl_wave,
            self.lbl_enemies,
            self.lbl_traps,
        )

    def update(self, wave, enemies, traps):
        self.lbl_hp.set_text("Mood: {}%".format(self.player.hp), topleft=self.frame.topleft)
        self.lbl_score.set_text("Score: {}".format(self.player.score), topleft=self.lbl_hp.rect.bottomleft)
        self.lbl_wave.set_text("Wave: {}".format(wave), centerx=self.frame.centerx)
        self.lbl_enemies.set_text("Ghosts: {}/{}".format(wave - enemies, wave), topright=self.frame.topright)
        self.lbl_traps.set_text("Traps: {}/{}".format(wave + 1 - traps, wave + 1),
                                topright=self.lbl_enemies.rect.bottomright)

    def draw(self, surface):
        self.labels.draw(surface)
