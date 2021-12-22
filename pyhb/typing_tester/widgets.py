import pygame
from typing import Tuple


class Label:
    def __init__(
        self,
        position,
        size,
        content: str,
        colour=None,
        border_colour=None,
        txt_colour=(255, 255, 255),
        shape="rectangle",
    ):
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        # self.surface.set_colorkey((0, 0, 0))
        self.content = content

        self.colour = colour or None
        self.border_colour = border_colour or None
        self.txt_colour = txt_colour
        self.shape = shape
        self.t = pygame.font.SysFont("arial", size=self.rect.size[0] // 8).render(
            content, True, self.txt_colour
        )

    def draw(self, screen: pygame.Surface):
        if self.colour:
            if self.shape == "rectangle":
                pygame.draw.rect(
                    self.surface,
                    self.colour,
                    self.surface.get_rect(),
                    border_radius=1,
                    width=5,
                )
        if self.border_colour:
            pygame.draw.rect(
                self.surface,
                self.border_colour,
                self.surface.get_rect(),
                border_radius=4,
                width=1,
            )

        screen.blit(self.surface, self.rect)
        screen.blit(self.t, self.t.get_rect(center=self.rect.center))


class Toggle:
    def __init__(self, size: Tuple[int, int]):
        self.size = size

        # Make rounded Surface
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0, 0, 0))
        self.grey = 100
        self.color = pygame.Color((self.grey, self.grey, self.grey))
        self.rect = pygame.Rect((0, 0), self.size)
        self.pos_rect = pygame.Rect((0, 0), self.size)

        # Flags
        self.switch = False
        self.transition = False

        # Count variables
        self.dt = 0

    def update(self, dt):
        self.dt = dt

    def draw(self, screen: pygame.Surface, pos: Tuple[int, int]):
        self.surf.fill((0, 0, 0))
        # s_rect = screen.get_rect()

        self.pos_rect.topleft = pos

        pygame.draw.rect(self.surf, self.color, self.rect)
        radius = self.size[1] // 2
        pygame.draw.circle(screen, self.color, self.pos_rect.midleft, radius)
        pygame.draw.circle(screen, self.color, self.pos_rect.midright, radius)

        screen.blit(self.surf, pos)


class ThemeSelection:
    ...



