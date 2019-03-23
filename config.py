from pygame import Color


SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (900, 680)
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

ENEMY_SIZE = (ENEMY_WIDTH, ENEMY_HEIGHT) = (64, 64)
ENEMY_COLOR = Color('#17FF64')
ENEMY_SPEED = 7
ENEMY_BORDER = 20
ENEMY_FRAME_SIZE = (ENEMY_WIDTH + ENEMY_BORDER * 2, ENEMY_HEIGHT + ENEMY_BORDER * 2)
ENEMY_SHOOT_TIMEOUT = 20
ENEMY_VEER_TIMEOUT = (100, 300)

DAMAGE_PLASMA_SIZE = (DAMAGE_PLASMA_WIDTH, DAMAGE_PLASMA_HEIGHT) = (16, 16)
DAMAGE_PLASMA_SPEED = 15
DAMAGE_PLASMA_COLOR = Color('#00FF3B')
DAMAGE_PLASMA_OFFSET = (-25, -15)

HEALER_SIZE = (HEALER_WIDTH, HEALER_HEIGHT) = (64, 64)
HEALER_COLOR = Color('#3311CC')
HEALER_SPEED = 9
HEALER_BORDER = 20
HEALER_FRAME_SIZE = (HEALER_WIDTH + HEALER_BORDER * 2, HEALER_HEIGHT + HEALER_BORDER * 2)
HEALER_SHOOT_TIMEOUT = 40
HEALER_VEER_TIMEOUT = (150, 360)

HEAL_PLASMA_SIZE = (HEAL_PLASMA_WIDTH, HEAL_PLASMA_HEIGHT) = (20, 20)
HEAL_PLASMA_SPEED = 15
HEAL_PLASMA_COLOR = Color('#003BFF')
HEAL_PLASMA_OFFSET = (10, 20)

BOMB_SIZE = (BOMB_WIDTH, BOMB_HEIGHT) = (22, 30)
BOMB_COLOR = Color('#22DD11')
BOMB_TIMEOUT = 120
