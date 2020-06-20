# Copyright (C) 2019-2020, Daniel Efimenko
#
# This file is part of Haunted_Library.
#
# Haunted_Library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Haunted_Library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Haunted_Library.  If not, see <https://www.gnu.org/licenses/>.
#

"""Файл игровых констант.

Здесь описаны игровые константы, изменяя
которые, можно изменять поведение игры.
Дробные значения относительны.
Целые значения могут быть только целыми.
Значения задержек, длительностей - в миллисекундах.
Значения расстояний - в пикселях.
В диапазонах должен соблюдаться порядок (меньшее, большее).
Изменение значения на некорректное может сломать игру.
"""

from os.path import exists as file_exists
from configparser import ConfigParser
from math import sqrt

from pygame import Color
from pygame.display import Info as DisplayInfo

def _read_range(section, key, default, type_, polarity=1):
    value = _settings[section].get(key, default).replace(' ', '')
    value = list(map(lambda x: polarity * type_(x), value.split(',')))
    value.sort()
    return tuple(value)

_settings = ConfigParser()
if not _settings.read('./settings.ini', 'utf-8'):
    print("Файл с пользовательскими настройками(settings.ini) не обнаружен, ищем настройки по умолчанию.")
    if not _settings.read('./utils/default_settings.ini', 'utf-8'):
        print("Не найден файл с настройками по умолчанию(utils/default_settings.ini), до свидания.")
        raise SystemExit

_default_settings = ConfigParser()
_default_settings.read('./utils/default_settings.ini', 'utf-8')
for section in _default_settings:
    if section not in _settings:
        _settings[section] = {}

# Экран
UNIT_SCALE = _settings['screen'].getfloat('unit_scale', 1.9)
FPS = 60  # Макс. кол-во кадров в секунду
#-------------------------------------------------------------------------------

# Служебное, тут лучше ничего не менять.
_di = DisplayInfo()
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (_di.current_w, _di.current_h)
UNIT_SCALE = sqrt(UNIT_SCALE)
scaled = lambda val: val * UNIT_SCALE  # масштабирует значение
rscaled = lambda val: round(scaled(val))  # матабирует и округляет значение
size_rscaled = lambda size: tuple(map(rscaled, size))  # масштабирует и округляет последовательность
WALL_WIDTH = rscaled(50)
WALL_HEIGHT = rscaled(50)
WALL_SIZE = (WALL_WIDTH, WALL_HEIGHT)
TOTAL_LEVEL_SIZE = (WALL_WIDTH * 50, WALL_HEIGHT * 50)
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
#-------------------------------------------------------------------------------

# Меню
MENU_BG_COLOR = Color('#333377')  # Цвет фона
MENU_BTN_SIZE = (MENU_BTN_WIDTH, MENU_BTN_HEIGHT) = (500, 160)  # Размер кнопок
MENU_BTN_FONT_SIZE = 60  # Размер шрифта кнопок
#-------------------------------------------------------------------------------

# Кнопки
BTN_TXT_USUAL_COLOR = Color('#FFFFFF')   # Цвет обычного текста для кнопок
BTN_TXT_SELECTED_COLOR = Color('#FF8888')   # Цвет текста кнопки, когда она под курсором
BTN_TXT_INACTIVE_COLOR = Color('#AAAAAA')   # Цвет текста кнопки, когда она не активна
BTN_BG_COLOR = Color('#555577')   # Цвет фона кнопки
#-------------------------------------------------------------------------------

# Текстовые метки
LBL_TXT_DEFAULT_COLOR = Color('#FFFFFF')   # Цвет обычного текста меток
#-------------------------------------------------------------------------------

# Игрок
PLAYER_SPEED = scaled(_settings['player'].getfloat('speed', 0.48))
PLAYER_HP_MAX = _settings['player'].getint('hp', 100)
PLAYER_PLASMA_SPEED = scaled(_settings['player'].getfloat('plasma_speed', 0.9))
PLAYER_PLASMA_OFFSET = _read_range('player', 'plasma_damage', '15, 25', int, -1)
#-------------------------------------------------------------------------------

# Привидение
ENEMY_SPEED = scaled(_settings['ghost'].getfloat('speed', 0.43))
ENEMY_FRAME_SIZE = size_rscaled((94, 94))   # Размер рамки для столкновений
ENEMY_SHOOT_TIMEOUT = _settings['ghost'].getint('shoot_timeout', 600)
ENEMY_VEER_TIMEOUT = _read_range('ghost', 'veer_timeout', '1700, 4300', int)
ENEMY_MAX_SHOOT_DISTANCE = rscaled(_settings['ghost'].getint('max_shoot_distance', 600))
ENEMY_HP_MAX = _settings['ghost'].getint('hp', 100)
ENEMY_HP_SHOWING_TIMEOUT = 4000   # Длительность отображения здоровья
ENEMY_PLASMA_SPEED = scaled(_settings['ghost'].getfloat('plasma_speed', 0.8))
ENEMY_PLASMA_OFFSET = _read_range('ghost', 'plasma_damage', '5, 15', int, -1)
#-------------------------------------------------------------------------------

# Привидение-босс
BOSS_ENEMY_SPEED = scaled(_settings['bossghost'].getfloat('speed', 0.4))
BOSS_ENEMY_FRAME_SIZE = size_rscaled((100, 100))   # Размер рамки для столкновений
BOSS_ENEMY_SHOOT_TIMEOUT = _settings['bossghost'].getint('shoot_timeout', 700)
BOSS_ENEMY_VEER_TIMEOUT = _read_range('bossghost', 'veer_timeout', '2000, 4500', int)
BOSS_ENEMY_HP_MAX = _settings['bossghost'].getint('hp', 300)
BOSS_ENEMY_SPAWN_DELAY = _settings['bossghost'].getint('spawn', 3)
BOSS_ENEMY_PLASMA_SPEED = scaled(_settings['bossghost'].getfloat('plasma_speed', 0.75))
BOSS_ENEMY_PLASMA_OFFSET = _read_range('bossghost', 'plasma_damage', '10, 20', int, -1)
#-------------------------------------------------------------------------------

# Капкан
TRAP_OFFSET = -_settings['trap'].getint('damage', 33)
TRAP_ANIM_TIMEOUT = 333   # Задержка анимации
#-------------------------------------------------------------------------------

# Телепорт
TELEPORT_ANIM_TIMEOUT = 200   # Задержка анимации
#-------------------------------------------------------------------------------

# Датчик ПК-активности
PKL_MAX_DISTANCE = rscaled(1700)   # Макс. расстояние обнаружения
PKL_UPDATE_TIMEOUT = 500   # Задержка между обновлениями значения
#-------------------------------------------------------------------------------

# Сгустки позитива
HEALTHPOINT_OFFSET_RANGE = _read_range('healthpoint', 'heal', '17, 25', int)
HEALTHPOINT_NUMBER = _settings['healthpoint'].getint('number', 2)
#-------------------------------------------------------------------------------

# Мебель
FURNITURE_HP = 100   # Здоровье
#-------------------------------------------------------------------------------
