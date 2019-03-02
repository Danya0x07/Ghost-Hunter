from pygame import (init, display, event, time, Surface, Color)
from pygame.sprite import Group
from pygame.locals import *

import maps
from objects import Wall, Camera
from settings import *


class MainScene:

    def __init__(self, hunter):
        init()
        self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display.set_caption("Ghost&Hunter")
        self.bg = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg.fill(Color('#000077'))
        self.timer = time.Clock()
        self.hunter = hunter
        self.entities = Group(self.hunter)
        self.walls = []
        self.camera = Camera(*MainScene.get_total_level_size(maps.hotel_map))

    @staticmethod
    def get_total_level_size(level):
        t_width = len(level[0]) * WALL_LENGTH
        t_height = len(level) * WALL_LENGTH
        return t_width, t_height

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN:
                if e.key == K_w: self.hunter.dir.w = True
                if e.key == K_s: self.hunter.dir.s = True
                if e.key == K_a: self.hunter.dir.a = True
                if e.key == K_d: self.hunter.dir.d = True
            if e.type == KEYUP:
                if e.key == K_w: self.hunter.dir.w = False
                if e.key == K_s: self.hunter.dir.s = False
                if e.key == K_a: self.hunter.dir.a = False
                if e.key == K_d: self.hunter.dir.d = False

    def create_map(self):
        x = y = 0
        for row in maps.hotel_map:
            for col in row:
                if col == '-':
                    wall = Wall(x, y)
                    self.entities.add(wall)
                    self.walls.append(wall)
                x += WALL_LENGTH
            y += WALL_LENGTH
            x = 0

    def mainloop(self):
        self.create_map()
        while True:
            self.check_events()
            self.screen.blit(self.bg, (0, 0))
            self.hunter.update()
            self.camera.update(self.hunter)
            for e in self.entities:
                self.screen.blit(e.image, self.camera.apply(e))
            self.timer.tick(60)
            display.update()