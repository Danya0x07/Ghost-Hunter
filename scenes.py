from pygame import display, event, mouse, Surface
from pygame.sprite import Group
from pygame.time import Clock
from pygame.locals import *
from tiledtmxloader import tmxreader, helperspygame

from interface import Button, Label, DataDisplayer
from decor import Sofa, Flower
from camera import Camera
from player import Player
from enemy import Enemy, BossEnemy
from teleport import Teleport
from health import HealthPoint
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
            display.flip()
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

        self.lbl_title = Label('Haunted Library', fontsize=70,
                               centerx=self.screen_rect.centerx,
                               centery=130)
        self.lbl_v = Label('v1.0', fontsize=20,
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
        super().__init__(screen, (0, 0, 0))
        self.walls = []
        self.enemy_spawn_positions = []
        self.hp_spawn_positions = []
        self.animations = []
        self.furniture = Group()
        self.enemies = Group()
        self.plasmas = Group()
        self.traps = Group()
        self.teleports = Group()
        self.healthpoints = Group()
        self.camera = Camera(TOTAL_LEVEL_SIZE)
        self.create_map('library_map_2.tmx')
        self.stats = DataDisplayer()
        self.wave = 0

    def create_map(self, mapname):
        world_map = tmxreader.TileMapParser().parse_decode("resources/{}".format(mapname))
        resources = helperspygame.ResourceLoaderPygame()
        resources.load(world_map)
        layers = helperspygame.get_layers_from_map(resources)
        self.bg_layer = layers[0]
        obj_layer = layers[1]
        for obj in obj_layer.objects:
            obj_type = obj.properties['type']
            if obj_type == 'player':
                self.player = Player(obj.x, obj.y - WALL_HEIGHT)
            elif obj_type == 'wall':
                self.walls.append(Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj_type == 'teleport':
                s_id = obj.properties['id']
                tgt_id = obj.properties['tgt_id']
                self.teleports.add(Teleport(obj.x, obj.y - WALL_HEIGHT, s_id, tgt_id))
            elif obj_type == 'gspawn':
                self.enemy_spawn_positions.append((obj.x, obj.y - WALL_HEIGHT))
            elif obj_type == 'hspawn':
                self.hp_spawn_positions.append((obj.x, obj.y - WALL_HEIGHT))
            elif obj_type == 'sofa':
                self.furniture.add(Sofa(obj.x, obj.y))
            elif obj_type == 'flower':
                self.furniture.add(Flower(obj.x, obj.y - WALL_HEIGHT))
        self.renderer = helperspygame.RendererPygame()
        HealthPoint.random_spawn(self.hp_spawn_positions, self.healthpoints, HEALTHPOINT_NUMBER)

    def check_events(self):
        for e in event.get():
            if e.type == QUIT:
                raise SystemExit
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.return_code = 'tomenu'
                elif e.key == K_SPACE:
                    self.player.handle_trap(self.traps, self.wave)
                else:
                    self.player.set_direction(e.key, True)
            elif e.type == KEYUP:
                self.player.set_direction(e.key, False)
            elif e.type == MOUSEBUTTONDOWN:
                self.player.shoot(self.camera.apply(self.player), mouse.get_pos(), self.plasmas)

        if not self.player.is_alive:
            self.return_code = 'gameover'
        if len(self.enemies) == 0:
            self.wave += 1
            self.traps.empty()
            if self.wave % BOSS_ENEMY_SPAWN_DELAY == 0:
                BossEnemy.random_spawn(self.enemy_spawn_positions, self.enemies, 1)
                Enemy.random_spawn(self.enemy_spawn_positions, self.enemies, self.wave - 1)
            else:
                Enemy.random_spawn(self.enemy_spawn_positions, self.enemies, self.wave)

    def update_objects(self):
        self.furniture.update(self)
        self.player.update(self)
        self.enemies.update(self)
        self.plasmas.update(self)
        self.traps.update(self)
        self.teleports.update(self)
        self.healthpoints.update(self)
        self.camera.update(self.player)
        ctr_offset = self.camera.reverse(CENTER_OF_SCREEN)
        self.renderer.set_camera_position_and_size(ctr_offset[0], ctr_offset[1],
                                                   *SCREEN_SIZE, "center")
        self.stats.update(self)

    def draw_group(self, group):
        for obj in group:
            self.screen.blit(obj.image, self.camera.apply(obj))

    def draw_objects(self):
        self.renderer.render_layer(self.screen, self.bg_layer)
        self.draw_group(self.furniture)
        self.draw_group(self.teleports)
        self.draw_group(self.healthpoints)
        self.draw_group(self.traps)
        self.draw_group(self.plasmas)
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.draw_group(self.enemies)
        for e in self.enemies:
            e.lbl_hp_showing_timer.update(self)
        for a in self.animations:
            a.update(self.screen, self.camera)
            if a.lifetime <= 0:
                self.animations.remove(a)
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
