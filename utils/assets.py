from pygame.image import load
from pygame.mixer import Sound
from pygame.transform import rotate
from pyganim import getImagesFromSpriteSheet


print("Загрузка ресурсов...")

p_img = load('resources/hunter.png')
player_images = (p_img, rotate(p_img, 90), rotate(p_img, 180), rotate(p_img, 270))

enemy_plasma_image = load('resources/gplasma.png')
boss_enemy_plasma_image = load('resources/bgplasma.png')
player_plasma_image = load('resources/pplasma.png')

heal_image = load('resources/heal.png')

enemy_images = getImagesFromSpriteSheet('resources/ghost.png',
    64, 64, 1, 4, [(0, 0, 64, 64),
                   (64, 0, 64, 64),
                   (128, 0, 64, 64),
                   (192, 0, 64, 64)]
)

boss_enemy_images = getImagesFromSpriteSheet('resources/bossghost.png',
    70, 70, 1, 4, [(0, 0, 70, 70),
                   (70, 0, 70, 70),
                   (140, 0, 70, 70),
                   (210, 0, 70, 70)]
)

sofa_images = getImagesFromSpriteSheet('resources/sofa.png',
    100, 50, 3, 1, [(0, 0, 100, 50),
                    (0, 50, 100, 50),
                    (0, 100, 100, 50)]
)

flower_images = getImagesFromSpriteSheet('resources/flower.png',
    50, 50, 1, 3, [(0, 0, 50, 50),
                   (50, 0, 50, 50),
                   (100, 0, 50, 50)]
)

teleport_images = getImagesFromSpriteSheet('resources/teleport.png',
    64, 64, 1, 4, [(0, 0, 64, 64),
                   (64, 0, 64, 64),
                   (128, 0, 64, 64),
                   (192, 0, 64, 64)]
)

trap_images = getImagesFromSpriteSheet('resources/trap.png',
    32, 32, 1, 2, [(0, 0, 32, 32),
                   (32, 0, 32, 32)]
)


enemy_dying_anim = getImagesFromSpriteSheet('resources/ghostdie.png',
    32, 32, 1, 3, [(0, 0, 32, 32),
                   (32, 0, 32, 32),
                   (64, 0, 32, 32)]
)

plasm_anim = getImagesFromSpriteSheet('resources/explasm.png',
    32, 32, 1, 3, [(0, 0, 32, 32),
                   (32, 0, 32, 32),
                   (64, 0, 32, 32)]
)

# звуки
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
