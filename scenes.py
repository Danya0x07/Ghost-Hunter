from pygame import display, event, mouse, Surface
from pygame.sprite import Group
from pygame.time import Clock
from pygame.locals import *

import maps
from maps import get_total_level_size
from interface_objects import Button, Label, DataDisplayer
from game_objects import Wall, Camera, Player, Enemy, Healer, Teleport
from config import *


class Scene:

    def __init__(self, screen, bg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.space = Surface(SCREEN_SIZE)
        self.space.fill(bg)
        self.clock = Clock()
        self.return_code = None

    def check_events(self):
        pass

    def update_objects(self):
        pass

    def draw_objects(self):
        pass

    def mainloop(self):
        self.return_code = None
        while self.return_code is None:
            self.check_events()
            self.update_objects()
            self.draw_objects()
            self.clock.tick(FPS)
            display.update()
        return self.return_code


class Menu(Scene):
    NUM_OF_BTNS = 3

    def __init__(self, screen):
        super().__init__(screen, MENU_BG_COLOR)
        self.frame_btn = Rect(0, 0, MENU_BTN_WIDTH, MENU_BTN_HEIGHT * Menu.NUM_OF_BTNS)
        self.frame_btn.centerx = self.screen_rect.centerx
        self.frame_btn.centery = self.screen_rect.centery + 50
        self.create_widgets()

    def create_widgets(self):
        self.btn_play     = Button("New Game", 'newgame',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 0, MENU_BTN_HEIGHT))
        self.btn_continue = Button("Continue", 'continue',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 1, MENU_BTN_HEIGHT), active=False)
        self.btn_quit     = Button("Quit", 'exit',
                                   rectsize=MENU_BTN_SIZE, fontsize=MENU_BTN_FONT_SIZE,
                                   topleft=Button.get_btn_pos(self.frame_btn, 2, MENU_BTN_HEIGHT))
        self.buttons = Group(self.btn_play, self.btn_continue, self.btn_quit)

        self.lbl_title = Label('Ghost&Hunter', fontsize=70,
                               centerx=self.screen_rect.centerx,
                               centery=130)
        self.lbl_v = Label('v0.1', fontsize=20,
                           bottomright=self.screen_rect.bottomright)
        self.labels = Group(self.lbl_title, self.lbl_v)

    def handle_buttons(self, position):
        for btn in self.buttons:
            if btn.check_pressed(position):
                self.return_code = btn.id
                if btn.id == 'newgame':
                    self.btn_continue.active = True

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                self.return_code = 'exit'
            elif e.type == MOUSEBUTTONDOWN:
                self.handle_buttons(e.pos)

    def update_objects(self):
        self.buttons.update(mouse.get_pos())

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.labels.draw(self.screen)
        for btn in self.buttons:
            btn.draw(self.screen)


class MainScene(Scene):

    def __init__(self, screen):
        super().__init__(screen, GAME_BG_COLOR)
        self.walls = Group()
        self.enemies = Group()
        self.healers = Group()
        self.plasmas = Group()
        self.bombs = Group()
        self.teleports = Group()
        self.camera = Camera(get_total_level_size(maps.hotel_map))
        self.create_map(maps.hotel_map)
        self.stats = DataDisplayer(self.player, self.screen_rect)

    def create_map(self, level_map):
        x = y = 0
        for row in level_map:
            for col in row:
                if col == '#':
                    self.walls.add(Wall(x, y))
                elif col == 'p':
                    self.player = Player(x, y)
                elif col == 'e':
                    self.enemies.add(Enemy(x, y))
                elif col == 'h':
                    self.healers.add(Healer(x, y))
                elif col == '1':
                    self.teleports.add(Teleport(x, y, '1', '2'))
                elif col == '2':
                    self.teleports.add(Teleport(x, y, '2', '1'))
                x += WALL_WIDTH
            y += WALL_HEIGHT
            x = 0

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.return_code = 'tomenu'
                elif e.key == K_SPACE:
                    self.player.lay_bomb(self.bombs)
                else:
                    self.player.set_direction(e.key, True)
            elif e.type == KEYUP:
                self.player.set_direction(e.key, False)

    def update_objects(self):
        self.player.update(self.walls)
        self.enemies.update(self.walls, self.plasmas)
        self.healers.update(self.walls, self.plasmas)
        self.plasmas.update(self.walls, self.plasmas, self.player)
        self.bombs.update(self.enemies, self.healers, self.bombs, self.player)
        self.teleports.update(self.player, self.enemies, self.healers, self.teleports)
        self.camera.update(self.player)
        self.stats.update()
        if not self.player.is_alive:
            self.return_code = 'gameover'

    def draw_group(self, group):
        for obj in group:
            self.screen.blit(obj.image, self.camera.apply(obj))

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.draw_group(self.walls)
        self.draw_group(self.teleports)
        self.draw_group(self.bombs)
        self.draw_group(self.plasmas)
        self.draw_group(self.healers)
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.draw_group(self.enemies)
        self.stats.draw(self.screen)


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
