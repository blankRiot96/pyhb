import pygame
import os
from typing import Tuple


class Settings:
    def __init__(self) -> None:
        # Path to which 'pyhb' is installed 
        self.user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        # print(self.user_path + '/settings_icon.png')
        self.icon = pygame.image.load(self.user_path + '/settings_icon.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (40, 40))
        self.rect = self.icon.get_rect(center=(25, 25))

    def update(self, mouse_pos: Tuple[int, int], events, dt) -> None:
        
        hover = self.rect.collidepoint(mouse_pos)
        for event in events:
            if hover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('Ok')

    def draw(self, screen) -> None:
        screen.blit(self.icon, self.rect)
    

