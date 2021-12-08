import pygame
from pygame._sdl2 import Window

pygame.init()

clock = pygame.time.Clock()
FPS = 60

screen_width = 1100
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
# screen = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption('HeartBeat Typing Test')

# Setting SDL2 Window and its opacity
window = Window.from_display_module()
window.opacity = 0.8
