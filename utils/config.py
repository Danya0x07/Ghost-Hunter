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

from math import sqrt

from pygame import Color
from pygame.display import Info as DisplayInfo


# Экран
UNIT_SCALE = 1.9  # Масштаб
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
PLAYER_SPEED = scaled(0.48)   # Скорость перемещения
PLAYER_HP_MAX = 100   # Здоровье
PLAYER_PLASMA_SPEED = scaled(0.9)   # Скорость плазмы
PLAYER_PLASMA_OFFSET = (-25, -15)   # Диапазон урона от плазмы
#-------------------------------------------------------------------------------

# Привидение
ENEMY_SPEED = scaled(0.43)   # Скорость перемещения
ENEMY_FRAME_SIZE = size_rscaled((94, 94))   # Размер рамки для столкновений
ENEMY_SHOOT_TIMEOUT = 600   # Задержка между выстрелами
ENEMY_VEER_TIMEOUT = (1700, 4300)   # Диапазон задержки между автоматическими сменами курса
ENEMY_MAX_SHOOT_DISTANCE = rscaled(600)   # Макс. дальнобойность
ENEMY_HP_MAX = 100   # Здоровье
ENEMY_HP_SHOWING_TIMEOUT = 4000   # Длительность отображения здоровья
ENEMY_PLASMA_SPEED = scaled(0.8)   # Скорость плазмы
ENEMY_PLASMA_OFFSET = (-15, -5)   # Диапазон урона от плазмы
#-------------------------------------------------------------------------------

# Привидение-босс
BOSS_ENEMY_SPEED = scaled(0.4)   # Скорость перемещения
BOSS_ENEMY_FRAME_SIZE = size_rscaled((100, 100))   # Размер рамки для столкновений
BOSS_ENEMY_SHOOT_TIMEOUT = 700   # Задержка между выстрелами
BOSS_ENEMY_VEER_TIMEOUT = (2000, 4500)   # Диапазон задержки между автоматическими сменами курса
BOSS_ENEMY_HP_MAX = 300   # Здоровье
BOSS_ENEMY_SPAWN_DELAY = 3   # Раз во сколько волн появляется
BOSS_ENEMY_PLASMA_SPEED = scaled(0.75)   # Скорость плазмы
BOSS_ENEMY_PLASMA_OFFSET = (-20, -10)   # Диапазон урона от плазмы
#-------------------------------------------------------------------------------

# Капкан
TRAP_OFFSET = -33   # Урон
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
HEALTHPOINT_OFFSET_RANGE = (17, 25)   # Диапазон
HEALTHPOINT_NUMBER = 2   # Постоянное кол-во на карте
#-------------------------------------------------------------------------------

# Мебель
FURNITURE_HP = 100   # Здоровье
#-------------------------------------------------------------------------------
