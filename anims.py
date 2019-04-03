from pyganim import getImagesFromSpriteSheet

ENEMY_DYING = getImagesFromSpriteSheet('resources/ghostdie.png', 32, 32, 1, 3, [(0, 0, 32, 32),
                                                                                (32, 0, 32, 32),
                                                                                (64, 0, 32, 32)])

PLASM_ANIM = getImagesFromSpriteSheet('resources/explasm.png', 32, 32, 1, 3, [(0, 0, 32, 32),
                                                                           (32, 0, 32, 32),
                                                                           (64, 0, 32, 32)])