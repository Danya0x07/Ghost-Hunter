from pygame import display, event, mouse, Surface, Color
from pygame.sprite import Group
from pygame.time import Clock
from pygame.locals import *

import maps
from maps import get_total_level_size
from objects import Wall, Camera, Hunter, Button
from settings import *


class Menu:
    NUM_OF_BTNS = 3

    def __init__(self, screen):
        self.screen = screen
        self.space = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.space.fill(Color('#333377'))
        self.clock = Clock()
        self.buttons = Group()
        self.frame_btn = Rect(0, 0, BTN_WIDTH, BTN_HEIGHT * Menu.NUM_OF_BTNS)
        self.frame_btn.center = self.screen.get_rect().center
        self.create_buttons()
        self.return_code = None

    def create_buttons(self):
        self.btn_play = Button("New Game", 'newgame',      Button.get_btn_pos(self.frame_btn, 0))
        self.btn_continue = Button("Continue", 'continue', Button.get_btn_pos(self.frame_btn, 1), active=False)
        self.btn_quit = Button("Quit", 'exit',             Button.get_btn_pos(self.frame_btn, 2))
        self.buttons.add(self.btn_play, self.btn_continue, self.btn_quit)

    def handle_buttons(self, position):
        for btn in iter(self.buttons):
            if btn.check_pressed(position):
                self.return_code = btn.id
                print(btn.id)
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
        for btn in iter(self.buttons):
            btn.draw(self.space)
        self.screen.blit(self.space, (0, 0))

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
        self.space.fill(Color('#000077'))
        self.hunter = Hunter(0, 0)
        self.entities = Group(self.hunter)
        self.walls = []
        self.camera = Camera(*get_total_level_size(maps.hotel_map))
        self.clock = Clock()
        self.create_map(maps.hotel_map)
        self.running = True

    def create_map(self, level_map):
        x = y = 0
        for row in level_map:
            for col in row:
                if col == '-':
                    wall = Wall(x, y)
                    self.entities.add(wall)
                    self.walls.append(wall)
                x += WALL_LENGTH
            y += WALL_LENGTH
            x = 0

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.running = False
                    return
                self.hunter.set_direction(e.key, True)
            elif e.type == KEYUP:
                self.hunter.set_direction(e.key, False)

    def update_objects(self):
        self.hunter.update(self.walls)
        self.camera.update(self.hunter)

    def draw_objects(self):
        self.screen.blit(self.space, (0, 0))
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

    def mainloop(self):
        self.running = True
        while self.running:
            self.check_events()
            self.update_objects()
            self.draw_objects()
            self.clock.tick(60)
            display.update()
