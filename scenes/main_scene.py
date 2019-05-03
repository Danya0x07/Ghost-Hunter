from pygame import event, mouse
from pygame.sprite import Group
from pygame.locals import *
from third_party.tiledtmxloader import helperspygame, tmxreader

from scenes.scene import Scene
from objects.decor import Furniture
from objects.player import Player
from objects.enemy import Enemy, BossEnemy
from objects.teleport import Teleport
from objects.health import HealthPoint
from utils.camera import Camera
from utils.data_displayer import DataDisplayer
from utils.config import *


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
                self.furniture.add(Furniture('sofa', obj.x, obj.y))
            elif obj_type == 'flower':
                self.furniture.add(Furniture('flower', obj.x, obj.y - WALL_HEIGHT))
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

