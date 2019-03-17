from pygame import display, event, mouse, Surface
from pygame.sprite import Group
from pygame.time import Clock
from pygame.locals import *

import maps
from maps import get_total_level_size
from menu_objects import Button, Label
from game_objects import Wall, Camera, Hunter, Enemy
from config import *


class Menu:
    NUM_OF_BTNS = 3

    def __init__(self, screen):
        self.screen = screen
        self.space = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.space.fill(MENU_BG_COLOR)
        self.frame_btn = Rect(0, 0, BTN_WIDTH, BTN_HEIGHT * Menu.NUM_OF_BTNS)
        self.frame_btn.center = self.screen.get_rect().center
        self.create_widgets()
        self.clock = Clock()
        self.return_code = None

    def create_widgets(self):
        self.btn_play = Button("New Game", 'newgame', Button.get_btn_pos(self.frame_btn, 0))
        self.btn_continue = Button("Continue", 'continue', Button.get_btn_pos(self.frame_btn, 1), active=False)
        self.btn_quit = Button("Quit", 'exit', Button.get_btn_pos(self.frame_btn, 2))
        self.buttons = Group(self.btn_play, self.btn_continue, self.btn_quit)

        self.lbl_v = Label('v0.1', bottomright=self.screen.get_rect().bottomright)
        self.labels = Group(self.lbl_v)

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

    def mainloop(self):
        self.return_code = None
        while self.return_code is None:
            self.check_events()
            self.update_objects()
            self.draw_objects()
            self.clock.tick(60)
            display.update()
        return self.return_code


class MainScene:

    def __init__(self, screen):
        self.screen = screen
        self.space = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.space.fill(GAME_BG_COLOR)
        self.walls = Group()
        self.enemies = Group()
        self.plasmas = Group()
        self.bombs = Group()
        self.create_map(maps.hotel_map)
        self.camera = Camera(*get_total_level_size(maps.hotel_map))
        self.clock = Clock()
        self.return_code = None

    def create_map(self, level_map):
        x = y = 0
        for row in level_map:
            for col in row:
                if col == '#':
                    self.walls.add(Wall(x, y))
                elif col == 'h':
                    self.hunter = Hunter(x, y)
                elif col == 'e':
                    self.enemies.add(Enemy(x, y))
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
                    self.hunter.lay_bomb(self.bombs)
                else:
                    self.hunter.set_direction(e.key, True)
            elif e.type == KEYUP:
                self.hunter.set_direction(e.key, False)

    def update_objects(self):
        self.hunter.update(self.walls)
        self.enemies.update(self.walls, self.plasmas)
        self.plasmas.update(self.walls, self.plasmas)
        self.bombs.update(self.enemies, self.bombs, self.hunter)
        self.camera.update(self.hunter)
        if not self.hunter.is_alive:
            self.return_code = 'gameover'

    def draw_group(self, group):
        for obj in group:
            self.screen.blit(obj.image, self.camera.apply(obj))

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        self.draw_group(self.walls)
        self.draw_group(self.bombs)
        self.draw_group(self.plasmas)
        self.draw_group(self.enemies)
        self.screen.blit(self.hunter.image, self.camera.apply(self.hunter))

    def mainloop(self):
        self.return_code = None
        while self.return_code is None:
            self.check_events()
            self.update_objects()
            self.draw_objects()
            self.clock.tick(60)
            display.update()
        return self.return_code
