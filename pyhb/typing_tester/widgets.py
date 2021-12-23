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

        # Color variables
        self.grey = 100
        self.color = pygame.Color((self.grey, self.grey, self.grey))
        self.hover_border_color = pygame.Color("yellow")
        self.hover_border_width = 2

        # Rectangles
        self.rect = pygame.Rect((0, 0), self.size)
        self.pos_rect = pygame.Rect((0, 0), self.size)
        self.radius = self.size[1] // 2
        self.whole_rect = pygame.Rect(
            (0, 0), (self.rect.width + 2 * self.radius, self.rect.height)
        )
        self.hover_border_rect = pygame.Rect((0, 0),
                                             (self.size[0] + self.hover_border_width*2,
                                              self.size[1] + self.hover_border_width*2))

        # Flags
        self.switch = False
        self.transition = False
        self.hover = False

        # Count variables
        self.dt = 0

    def update(self, mouse_pos: Tuple[int, int], events, dt):
        self.dt = dt

        self.hover = self.whole_rect.collidepoint(mouse_pos)

        for event in events:
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Clicked")

    def draw(self, screen: pygame.Surface, pos: Tuple[int, int]):
        self.surf.fill((0, 0, 0))
        # s_rect = screen.get_rect()

        self.pos_rect.topleft = pos
        self.whole_rect.center = self.pos_rect.center
        self.hover_border_rect.center = self.pos_rect.center

        # Hover yellow borderline effect
        if self.hover:
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midleft,
                self.radius + self.hover_border_width,
            )
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midright,
                self.radius + self.hover_border_width)

            pygame.draw.rect(
                screen,
                self.hover_border_color,
                self.hover_border_rect)

        pygame.draw.circle(
            screen,
            self.color,
            self.pos_rect.midleft,
            self.radius,
        )
        pygame.draw.circle(screen, self.color, self.pos_rect.midright, self.radius)

        pygame.draw.rect(self.surf, self.color, self.rect)
        screen.blit(self.surf, pos)


class ThemeSelection:
    ...
