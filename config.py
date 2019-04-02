from pygame import Color


SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (970, 680)
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
WALL_SIZE = (WALL_WIDTH, WALL_HEIGHT) = (50, 50)
TOTAL_LEVEL_SIZE = (WALL_WIDTH * 50, WALL_HEIGHT * 50)
FPS = 60

MENU_BG_COLOR = Color('#333377')
MENU_BTN_SIZE = (MENU_BTN_WIDTH, MENU_BTN_HEIGHT) = (300, 100)
MENU_BTN_FONT_SIZE = 40

GAME_BG_COLOR = Color('#000000')

BTN_TXT_USUAL_COLOR = Color('#FFFFFF')
BTN_TXT_SELECTED_COLOR = Color('#FF8888')
BTN_TXT_INACTIVE_COLOR = Color('#AAAAAA')
BTN_BG_COLOR = Color('#555577')

LBL_TXT_DEFAULT_COLOR = Color('#FFFFFF')

PLAYER_SIZE = (PLAYER_WIDTH, PLAYER_HEIGHT) = (64, 64)
PLAYER_SPEED = 7
PLAYER_HP_MAX = 100

PLAYER_PLASMA_SIZE = (PLAYER_PLASMA_WIDTH, PLAYER_PLASMA_HEIGHT) = (20, 20)
PLAYER_PLASMA_SPEED = 15
PLAYER_PLASMA_OFFSET = (-25, -10)

ENEMY_SIZE = (ENEMY_WIDTH, ENEMY_HEIGHT) = (64, 64)
ENEMY_SPEED = 5
ENEMY_BORDER = 20
ENEMY_FRAME_SIZE = (ENEMY_WIDTH + ENEMY_BORDER * 2, ENEMY_HEIGHT + ENEMY_BORDER * 2)
ENEMY_SHOOT_TIMEOUT = 40
ENEMY_VEER_TIMEOUT = (100, 300)
ENEMY_MIN_SHOOT_DISTANCE = 400
ENEMY_HP_MAX = 100
ENEMY_HP_SHOWING_TIMEOUT = 180

BOSS_ENEMY_SIZE = (ENEMY_WIDTH, ENEMY_HEIGHT) = (70, 70)
BOSS_ENEMY_SPEED = 4
BOSS_ENEMY_BORDER = 20
BOSS_ENEMY_FRAME_SIZE = (ENEMY_WIDTH + ENEMY_BORDER * 2, ENEMY_HEIGHT + ENEMY_BORDER * 2)
BOSS_ENEMY_SHOOT_TIMEOUT = 30
BOSS_ENEMY_VEER_TIMEOUT = (100, 300)
BOSS_ENEMY_MIN_SHOOT_DISTANCE = 500
BOSS_ENEMY_HP_MAX = 300
BOSS_ENEMY_SPAWN_DELAY = 3

ENEMY_PLASMA_SPEED = 10
ENEMY_PLASMA_SIZE = (ENEMY_PLASMA_WIDTH, ENEMY_PLASMA_HEIGHT) = (16, 16)
ENEMY_PLASMA_OFFSET = (-15, -5)

BOSS_ENEMY_PLASMA_SIZE = (BOSS_ENEMY_PLASMA_WIDTH, BOSS_ENEMY_PLASMA_HEIGHT) = (26, 26)
BOSS_ENEMY_PLASMA_SPEED = 10
BOSS_ENEMY_PLASMA_OFFSET = (-20, -10)

TRAP_SIZE = (TRAP_WIDTH, TRAP_HEIGHT) = (32, 32)
TRAP_TIMEOUT = 40
TRAP_OFFSET = -15
TRAP_ANIM_TIMEOUT = FPS // 2

TELEPORT_SIZE = (TELEPORT_WIDTH, TELEPORT_HEIGHT) = (64, 64)
TELEPORT_ANIM_TIMEOUT = FPS // 4

PKL_MAX_DISTANCE = 1500
PKL_UPDATE_TIMEOUT = 60

HEALTHPOINT_SIZE = (HEALTHPOINT_WIDTH, HEALTHPOINT_HEIGHT) = (23, 23)
HEALTHPOINT_OFFSET_RANGE = (20, 30)
HEALTHPOINT_NUMBER = 2

FURNITURE_SIZE = (50, 50)
FURNITURE_HP = 100
