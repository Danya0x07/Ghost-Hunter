from pygame import event, mouse
from pygame.locals import *

from scenes.scene import Scene
from utils.interface import Button, Label
from utils.config import *

class GameOverScene(Scene):

    def __init__(self, screen, stats):
        super().__init__(screen, MENU_BG_COLOR)
        self.stats = stats
        self.btn_back = Button("to menu", 'tomenu',
                               rectsize=(150, 60), fontsize=24, bottomleft=(0, SCREEN_HEIGHT))
        self.lbl_gameover = Label("Game Over!", 50, midbottom=self.screen_rect.center)

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == MOUSEBUTTONDOWN:
                if self.btn_back.check_pressed(mouse.get_pos()):
                    self.return_code = self.btn_back.id

    def update_objects(self):
        self.btn_back.update(mouse.get_pos())

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.screen.blit(self.lbl_gameover.image, self.lbl_gameover.rect)
        self.btn_back.draw(self.screen)
        self.stats.draw(self.screen)
