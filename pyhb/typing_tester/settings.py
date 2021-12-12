import pygame
import os


class Settings:
    def __init__(self) -> None:
        # Path to which 'pyhb' is installed 
        self.user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        # print(self.user_path + '/settings_icon.png')
        self.icon = pygame.image.load(self.user_path + '/settings_icon.png')

    def update(self) -> None:
        pass

    def draw(self, screen) -> None:
        screen.blit(self.icon, (0, 0))
    

