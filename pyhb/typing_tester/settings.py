import pygame
import logging
import json
import math
import os
from typing import Tuple
from pyhb.typing_tester.widgets import Label, Toggle
from pyhb.typing_tester.themes import Theme


"""
Logging setup:-
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # setLevel to `NOTSET` before making a commit

file_handler = logging.FileHandler("debug_output/logger.txt")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def circle_surf(radius, color) -> pygame.Surface:
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))

    return surf


class Settings:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.theme = Theme("lavender")

        # Path to which 'pyhb' is installed
        self.user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        # print(self.user_path + '/settings_icon.png')
        self.img = pygame.image.load(
            self.user_path + "/assets/settings_icon.png"
        ).convert_alpha()
        self.icon = pygame.transform.scale(self.img, (40, 40))
        self.rect = self.icon.get_bounding_rect()
        self.rect.center = (30, 30)
        self.font = pygame.font.SysFont("arialrounded", 30)

        self.radius = 1

        # Settings Widgets
        self.label = Label(
            self.rect.center,
            (40 * 2.5, 10 * 2.5),
            "settings",
            colour="black",
            border_colour="white",
        )
        self.punctuation_toggle = Toggle((60, 20))

        # Surfaces
        self.punctuation_txt = self.font.render("Punctuation", True, "white")

        # Flags
        self.state = "typing_test"
        self.start_animation = False
        self.expanding = False
        self.hover = False

        # Animation variables
        self.transition_color = self.theme.settings_transition_color
        self.circle_animation = circle_surf(2, self.transition_color)
        self.circle_rect = self.circle_animation.get_rect(center=(-1000, -1000))
        self.pos = self.circle_rect.topleft
        self.ANIMATION_SPEED = 7
        self.dt = 0
        self.transition_distance = 0

        if os.path.exists(self.user_path + "/preferences.json"):
            with open(self.user_path + "/preferences.json") as f:
                self.preferences = json.load(f)
            self.theme = Theme(self.preferences["theme"])
        else:
            self.preferences = {
                "punctuation": False,
                "theme": self.theme._id,
                "duration": 30,
            }
            with open(self.user_path + "/preferences.json", "w") as f:
                json.dump(self.preferences, f, indent=2)

    def update(self, mouse_pos: Tuple[int, int], events, dt) -> None:
        """
        :param mouse_pos: Position of the mouse
        :param events: -> pygame.event.get()
        :param dt: Amount of time taken to complete last frame * FPS
        :return: None

        Updates the Settings class, and deals with position and data update related matter
        """

        self.dt = dt
        self.hover = self.rect.collidepoint(mouse_pos)
        for event in events:
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_animation = True
                    radius = self.screen.get_width()
                    self.circle_animation = circle_surf(radius, self.transition_color)
                    self.circle_rect = self.circle_animation.get_rect(
                        center=(-400, -400)
                    )
                    self.pos = list(self.circle_rect.topleft)
                    self.expanding = True

        if self.hover:
            self.label.rect.topleft = mouse_pos
            self.icon = pygame.transform.scale(self.img, (50, 50))
        else:
            self.icon = pygame.transform.scale(self.img, (40, 40))

        if self.start_animation:
            increment = self.ANIMATION_SPEED * self.dt
            increment_sqrd = increment ** 2
            if self.expanding:
                if self.transition_distance <= self.screen.get_width():
                    self.pos[0] += increment
                    self.pos[1] += increment

                    self.transition_distance += math.sqrt(
                        increment_sqrd + increment_sqrd
                    )

                    if self.ANIMATION_SPEED * self.dt == 0:
                        logger.error(
                            f"""
                            self.ANIMATION_SPEED\t={self.ANIMATION_SPEED},
                            dt\t={dt}
                            """
                        )
                        exit("debug at `if self.ANIMATION_SPEED * dt == 0`")
                else:
                    self.state = "settings"
                    self.expanding = False
            else:
                if self.transition_distance >= 0:
                    self.pos[0] -= increment
                    self.pos[1] -= increment

                    self.transition_distance -= math.sqrt(
                        increment_sqrd + increment_sqrd
                    )
                else:
                    self.start_animation = False
                    logger.info("END IS REACHED?")

        if self.state == "settings":
            self.punctuation_toggle.update(mouse_pos, events, dt)

    def save_preferences(self) -> None:
        """
        :return: None

        Save the user preferences
        """
        with open(self.user_path + "/preferences.json", "w") as f:
            json.dump(self.preferences, f, indent=2)

    def draw(self, screen: pygame.Surface) -> None:
        """
        :param screen: Screen to draw on.
        :return: None

        Deals with rendering the settings related widgets and graphics
        """
        s_rect = screen.get_rect()

        screen.blit(self.icon, self.rect)

        if self.hover:
            self.label.draw(screen)
            pygame.draw.circle(screen, "black", self.rect.center, self.radius)

        if self.start_animation:
            screen.blit(self.circle_animation, self.pos)

        # TODO: Render settings
        if self.state == "settings" and not self.start_animation:
            diff = 75
            punctuation_rect = self.punctuation_txt.get_rect(
                center=(s_rect.centerx - diff, s_rect.centery - 100)
            )
            screen.blit(self.punctuation_txt, punctuation_rect)
            self.punctuation_toggle.draw(
                screen, (s_rect.centerx + diff, punctuation_rect.centery - 7)
            )
