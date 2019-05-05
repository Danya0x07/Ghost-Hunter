from pygame.image import load
from pygame.mixer import Sound
from pygame.transform import rotate, scale
from pyganim import getImagesFromSpriteSheet

from utils.config import *


print("Загрузка ресурсов...")

# Текстуры
p_img = scale(load('resources/hunter.png'), sctu((64, 64)))
player_images = (p_img, rotate(p_img, 90), rotate(p_img, 180), rotate(p_img, 270))
enemy_plasma_image = scale(load('resources/gplasma.png'), sctu((16, 16)))
boss_enemy_plasma_image = scale(load('resources/bgplasma.png'), sctu((25, 25)))
player_plasma_image = scale(load('resources/pplasma.png'), sctu((22, 22)))
heal_image = scale(load('resources/heal.png'), sctu((25, 25)))

# Атласы текстур
enemy_images = [scale(img, sctu((64, 64))) for img in getImagesFromSpriteSheet('resources/ghost.png',
    64, 64, 1, 4, [(0, 0, 64, 64),
                   (64, 0, 64, 64),
                   (128, 0, 64, 64),
                   (192, 0, 64, 64)]
)]

boss_enemy_images = [scale(img, sctu((70, 70))) for img in getImagesFromSpriteSheet('resources/bossghost.png',
    70, 70, 1, 4, [(0, 0, 70, 70),
                   (70, 0, 70, 70),
                   (140, 0, 70, 70),
                   (210, 0, 70, 70)]
)]

sofa_images = [scale(img, sctu((100, 50))) for img in getImagesFromSpriteSheet('resources/sofa.png',
    100, 50, 3, 1, [(0, 0, 100, 50),
                    (0, 50, 100, 50),
                    (0, 100, 100, 50)]
)]

flower_images = [scale(img, sctu((50, 50))) for img in getImagesFromSpriteSheet('resources/flower.png',
    50, 50, 1, 3, [(0, 0, 50, 50),
                   (50, 0, 50, 50),
                   (100, 0, 50, 50)]
)]

teleport_images = [scale(img, sctu((64, 64))) for img in getImagesFromSpriteSheet('resources/teleport.png',
    64, 64, 1, 4, [(0, 0, 64, 64),
                   (64, 0, 64, 64),
                   (128, 0, 64, 64),
                   (192, 0, 64, 64)]
)]

trap_images = [scale(img, sctu((32, 32))) for img in getImagesFromSpriteSheet('resources/trap.png',
    32, 32, 1, 2, [(0, 0, 32, 32),
                   (32, 0, 32, 32)]
)]


enemy_dying_anim = [scale(img, sctu((32, 32))) for img in getImagesFromSpriteSheet('resources/ghostdie.png',
    32, 32, 1, 3, [(0, 0, 32, 32),
                   (32, 0, 32, 32),
                   (64, 0, 32, 32)]
)]

plasm_anim = [scale(img, sctu((32, 32))) for img in getImagesFromSpriteSheet('resources/explasm.png',
    32, 32, 1, 3, [(0, 0, 32, 32),
                   (32, 0, 32, 32),
                   (64, 0, 32, 32)]
)]

# Звуки
enemy_shoot_sound = Sound('resources/gshoot.wav')
enemy_auch_sound = Sound('resources/gauch.wav')
player_auch_sound = Sound('resources/auch.wav')
player_shoot_sound = Sound('resources/pshoot.wav')
player_walk_sound = Sound('resources/walk.wav')
trap_down_sound = Sound('resources/trapdown.wav')
trap_up_sound = Sound('resources/trapup.wav')
furniture_breaking_sound = Sound('resources/break.wav')
teleport_sound = Sound('resources/teleport.wav')
heal_sound = Sound('resources/heal.wav')


print("Готово.")
