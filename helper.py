import pygame
from const import *


def get_font(size):
    """
    Get font
    :param size: size of font
    :return:
    """
    return pygame.font.SysFont(FONT, size)
