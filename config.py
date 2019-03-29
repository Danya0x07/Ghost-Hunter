from pygame import Color


SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (970, 680)
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

WALL_SIZE = (WALL_WIDTH, WALL_HEIGHT) = (50, 50)
WALL_COLOR = Color('#703508')

PLAYER_SIZE = (PLAYER_WIDTH, PLAYER_HEIGHT) = (64, 64)
PLAYER_SPEED = 7
PLAYER_COLOR = Color('#AAAAAA')
PLAYER_HP_MAX = 1000

PLAYER_PLASMA_SIZE = (PLAYER_PLASMA_WIDTH, PLAYER_PLASMA_HEIGHT) = (20, 20)
PLAYER_PLASMA_SPEED = 13
PLAYER_PLASMA_COLOR = Color('#FF0000')
PLAYER_PLASMA_OFFSET = 10

ENEMY_SIZE = (ENEMY_WIDTH, ENEMY_HEIGHT) = (64, 64)
ENEMY_COLOR = Color('#17FF64')
ENEMY_SPEED = 5
ENEMY_BORDER = 20
ENEMY_FRAME_SIZE = (ENEMY_WIDTH + ENEMY_BORDER * 2, ENEMY_HEIGHT + ENEMY_BORDER * 2)
ENEMY_SHOOT_TIMEOUT = 40
ENEMY_VEER_TIMEOUT = (100, 300)
ENEMY_MIN_SHOOT_DISTANCE = 700
ENEMY_HP_MAX = 100
ENEMY_HP_SHOWING_TIMEOUT = 180

BOSS_ENEMY_SIZE = (ENEMY_WIDTH, ENEMY_HEIGHT) = (70, 70)
BOSS_ENEMY_COLOR = Color('#1766CC')
BOSS_ENEMY_SPEED = 4
BOSS_ENEMY_BORDER = 20
BOSS_ENEMY_FRAME_SIZE = (ENEMY_WIDTH + ENEMY_BORDER * 2, ENEMY_HEIGHT + ENEMY_BORDER * 2)
BOSS_ENEMY_SHOOT_TIMEOUT = 30
BOSS_ENEMY_VEER_TIMEOUT = (100, 300)
BOSS_ENEMY_MIN_SHOOT_DISTANCE = 700
BOSS_ENEMY_HP_MAX = 300

ENEMY_PLASMA_SPEED = 13
ENEMY_PLASMA_SIZE = (ENEMY_PLASMA_WIDTH, ENEMY_PLASMA_HEIGHT) = (16, 16)
ENEMY_PLASMA_COLOR = Color('#00FF3B')
ENEMY_PLASMA_OFFSET = (-25, -15)

BOSS_ENEMY_PLASMA_SIZE = (BOSS_ENEMY_PLASMA_WIDTH, BOSS_ENEMY_PLASMA_HEIGHT) = (26, 26)
BOSS_ENEMY_PLASMA_SPEED = 13
BOSS_ENEMY_PLASMA_COLOR = Color('#00FF3B')
BOSS_ENEMY_PLASMA_OFFSET = (-25, -15)

TRAP_SIZE = (TRAP_WIDTH, TRAP_HEIGHT) = (32, 32)
TRAP_COLOR = Color('#22DD11')
TRAP_TIMEOUT = 40

TELEPORT_SIZE = (TELEPORT_WIDTH, TELEPORT_HEIGHT) = (64, 64)
TELEPORT_COLOR = Color('#AA22EE')

PKL_MAX_DISTANCE = 2500
PKL_UPDATE_TIMEOUT = 60

HEALTHPOINT_SIZE = (HEALTHPOINT_WIDTH, HEALTHPOINT_HEIGHT) = (23, 23)
HEALTHPOINT_COLOR = Color('#7777FF')
HEALTHPOINT_OFFSET_RANGE = (20, 30)
HEALTHPOINT_NUMBER = 2

FURNITURE_SIZE = (70, 70)
FURNITURE_USUAL_COLOR = Color('#FFFF22')
FURNITURE_WORSE_COLOR = Color('#CCCC33')
FURNITURE_WORST_COLOR = Color('#888844')
FURNITURE_HP = 100
