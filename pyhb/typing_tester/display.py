"""
Contains display related configuration for the HeartBeat typing test
"""


import os
import json
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from pygame._sdl2 import Window

pygame.init()

clock = pygame.time.Clock()
FPS = 100


user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
with open(user_path + "/preferences.json") as f:
    preferences = json.load(f)

screen_width, screen_height = preferences["last_screen_size"]

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("HeartBeat Typing Test")

# Set icon
heart_icon = pygame.image.load(user_path + "/assets/pyhb_icon.png").convert_alpha()
pygame.display.set_icon(heart_icon)

# Setting SDL2 Window and its opacity
window = Window.from_display_module()
window.opacity = 0.8

# Hiding cursor
pygame.mouse.set_visible(False)
