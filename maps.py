from config import *


def get_total_level_size(level):
    width = len(level[0]) * WALL_WIDTH
    height = len(level) * WALL_HEIGHT
    return width, height


hotel_map = (
    "                --                                              ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                             ---                                ",
    "                                                 -              ",
    "                                                 -              ",
    "                                                 -              ",
    "                                                                ",
    "                  ---------                                     ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
    "                                                                ",
)
