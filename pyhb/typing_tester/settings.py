import pygame
import os
from typing import Tuple


def circle_surf(radius, color) -> pygame.Surface:
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))

    return surf


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
        # Use this to draw the button on the screen
        # As a placeholder, I draw its content, but it may be more complex
        # when you do it. Maybe you use images, maybe likely some background,
        # maybe some border and even shadows ?
        if self.colour:
            if self.shape == "rectangle":
                pygame.draw.rect(
                    self.surface, self.colour, self.surface.get_rect(), border_radius=1, width=5
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


class Settings:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        # Path to which 'pyhb' is installed
        self.user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        # print(self.user_path + '/settings_icon.png')
        self.img = pygame.image.load(
            self.user_path + "/settings_icon.png"
        ).convert_alpha()
        self.icon = pygame.transform.scale(self.img, (40, 40))
        self.rect = self.icon.get_bounding_rect()
        self.rect.center = (30, 30)

        self.state = "typing_test"
        self.start_animation = False
        self.radius = 1
        self.expanding = False
        self.label = Label(
            self.rect.center,
            (40*2.5, 10*2.5),
            "settings",
            colour="black",
            border_colour="white",
        )
        self.hover = False

        self.circle_animation = circle_surf(2, (1, 0, 0))
        self.circle_rect = self.circle_animation.get_rect(center=(-200, -200))

        self.ANIMATION_SPEED = 3

    def update(self, mouse_pos: Tuple[int, int], events, dt) -> None:
        self.hover = self.rect.collidepoint(mouse_pos)
        for event in events:
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_animation = True
                    radius = self.screen.get_width() + self.screen.get_height() // 2
                    self.circle_animation = circle_surf(radius, (1, 0, 0))
                    self.circle_rect = self.circle_animation.get_rect(center=(-200, -200))
                    self.expanding = True

        if self.hover:
            self.label.rect.topleft = mouse_pos
            self.icon = pygame.transform.scale(self.img, (50, 50))
        else:
            self.icon = pygame.transform.scale(self.img, (40, 40))

        if self.start_animation:
            x, y = self.screen.get_rect().center
            if self.expanding:
                if self.circle_rect.centerx < x and self.circle_rect.centery < y:
                    self.circle_rect.centerx += self.ANIMATION_SPEED
                    self.circle_rect.centery += self.ANIMATION_SPEED
                else:
                    self.state = "settings"
                    self.expanding = False
            else:
                vec_1 = pygame.Vector2(self.circle_rect.center)
                vec_2 = pygame.Vector2(self.screen.get_rect().center)
                if vec_1.distance_to(vec_2) < 500:
                    self.circle_rect.centerx -= self.ANIMATION_SPEED
                    self.circle_rect.centery -= self.ANIMATION_SPEED
                else:
                    self.start_animation = False

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.icon, self.rect)

        if self.hover:
            self.label.draw(screen)
            pygame.draw.circle(screen, "black", self.rect.center, self.radius)

        if self.start_animation:
            screen.blit(self.circle_animation, self.circle_rect)
