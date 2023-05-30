import pygame
from const import *


def get_font(size):
    """
    Get font
    :param size: size of font
    :return:
    """
    return pygame.font.SysFont(FONT, size)


def music_background():
    """
    Play music background
    :return:
    """
    pygame.mixer.music.load("Resourse/Sound/Wii music - Gaming background music.mp3")
    pygame.mixer.music.play(-1)


def sound_click_mouse():
    """
    play sound when click
    :return:
    """
    sound_click = pygame.mixer.Sound("Resourse/Sound/Click Sound.mp3")
    sound_click.play()


def sound_finish():
    """
    play sound when click
    :return:
    """
    sound_click = pygame.mixer.Sound("Resourse/Sound/Finish Sound.mp3")
    sound_click.play()
