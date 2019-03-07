from settings import *


def get_total_level_size(level):
    width = len(level[0]) * WALL_LENGTH
    height = len(level) * WALL_LENGTH
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
