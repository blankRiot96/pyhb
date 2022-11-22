import json
import math
import os
from typing import List, Tuple

import pygame

from pyhb.typing_tester.generic_types import ColorValue, Events, Pos, Size
from pyhb.typing_tester.themes import Theme
from pyhb.typing_tester.widgets import (DurationSelection, Label,
                                        ThemeSelection, Toggle)


def circle_surf(radius, color) -> pygame.Surface:
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))

    return surf


class Settings:
    """
    Settings object, renders settings and sets settings for the Typing Test application
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        # Path to which 'pyhb' is installed
        self.user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

        # Get preferences
        if os.path.exists(self.user_path + "/preferences.json"):
            with open(self.user_path + "/preferences.json") as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {
                "punctuation": False,
                "theme": "lavender",
                "duration": 30,
                "last_screen_size": [770, 456],
            }
            with open(self.user_path + "/preferences.json", "w") as f:
                json.dump(self.preferences, f, indent=2)

        # Make theme
        self.theme = Theme(self.preferences["theme"])

        # Settings icon
        self.settings_icon = pygame.image.load(
            self.user_path + "/assets/settings_icon.png"
        ).convert_alpha()
        self.retry_icon = pygame.image.load(
            self.user_path + "/assets/retry_icon.png"
        ).convert_alpha()

        self.img = self.settings_icon
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
        self.punctuation_toggle = Toggle((50, 20))
        self.theme_selector = ThemeSelection(self.theme)
        self.duration_selector = DurationSelection(
            self.theme, self.preferences["duration"]
        )

        # Surfaces
        self.punctuation_txt = self.font.render(
            "Punctuation", True, self.theme.font_color
        )
        self.theme_txt = self.font.render("Themes", True, self.theme.font_color)
        self.theme_txt_rect = self.theme_txt.get_rect()
        self.duration_txt = self.font.render("Duration", True, self.theme.font_color)

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

        # Themes selector
        self.mouse_pos = (0, 0)
        self.events = []

    def update(self, mouse_pos: Pos, events: Events, dt: float) -> None:
        """
        :param mouse_pos: Position of the mouse
        :param events: -> pygame.event.get()
        :param dt: Amount of time taken to complete last frame * FPS
        :return: None

        Updates the Settings class, and deals with position and data update related matter
        """

        self.dt = dt
        self.mouse_pos = mouse_pos
        self.events = events

        self.hover = self.rect.collidepoint(mouse_pos)
        for event in events:
            if self.hover:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_animation = True
                    radius = self.screen.get_width()
                    self.circle_animation = circle_surf(radius, self.transition_color)
                    self.circle_rect = self.circle_animation.get_rect(
                        center=(
                            -400 * (self.screen.get_width() / 700),
                            -400 * (self.screen.get_height() / 400),
                        )
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
            increment_sqrd = increment**2
            if self.expanding:
                if self.transition_distance <= self.screen.get_width():
                    self.pos[0] += increment * (self.screen.get_width() / 700)
                    self.pos[1] += increment * (self.screen.get_height() / 400)

                    self.transition_distance += math.sqrt(
                        increment_sqrd + increment_sqrd
                    )

                    if self.ANIMATION_SPEED * self.dt == 0:
                        exit("debug at `if self.ANIMATION_SPEED * dt == 0`")
                else:
                    if self.state == "typing_test":
                        self.state = "settings"
                    elif self.state == "settings":
                        self.state = "typing_test"
                    self.expanding = False
            else:
                if self.transition_distance >= 0:
                    self.pos[0] -= increment * (self.screen.get_width() / 700)
                    self.pos[1] -= increment * (self.screen.get_height() / 400)

                    self.transition_distance -= math.sqrt(
                        increment_sqrd + increment_sqrd
                    )
                else:
                    self.start_animation = False

        if self.state == "settings":
            self.punctuation_toggle.update(mouse_pos, events, dt)

    def save_preferences(self, last_screen_size: List[int]) -> None:
        """
        :return: None

        Save the user preferences
        """
        self.preferences["last_screen_size"] = last_screen_size

        with open(self.user_path + "/preferences.json", "w") as f:
            json.dump(self.preferences, f, indent=2)

    def draw(self, screen: pygame.Surface, resize_frame: bool) -> None:
        """
        :param screen: Screen to draw on.
        :param resize_frame: Bool if current frame is resized
        :return: None

        Deals with rendering the settings related widgets and graphics
        """
        s_rect = screen.get_rect()
        self.theme_txt_rect.center = (
            s_rect.centerx,
            s_rect.centery - self.theme_selector.theme_widget_size[0] * 3,
        )

        screen.blit(self.icon, self.rect)

        if self.hover:
            self.label.draw(screen)
            pygame.draw.circle(screen, "black", self.rect.center, self.radius)

        if self.start_animation:
            screen.blit(self.circle_animation, self.pos)

        # TODO: Render Themes settings
        if self.state == "settings" and not self.start_animation:

            # Punctuation Toggle
            diff = 75
            punctuation_rect = self.punctuation_txt.get_rect(
                center=(s_rect.centerx - diff, s_rect.midtop[1] + 60)
            )
            screen.blit(self.punctuation_txt, punctuation_rect)
            self.punctuation_toggle.draw(
                screen,
                (s_rect.centerx + diff, punctuation_rect.centery - 7),
                resize_frame,
            )
            self.preferences["punctuation"] = self.punctuation_toggle.switch

            # Theme Selection
            screen.blit(self.theme_txt, self.theme_txt_rect)
            self.theme_selector.draw(screen, self.mouse_pos, s_rect.center, self.events)
            self.theme = self.theme_selector.theme
            self.preferences["theme"] = self.theme._id

            # Duration Choice
            self.duration_txt = self.font.render(
                "Duration", True, self.theme.font_color
            )
            duration_rect = self.duration_txt.get_rect()
            duration_rect.center = (
                s_rect.midbottom[0],
                s_rect.midbottom[1] - 120 - self.font.get_height(),
            )

            screen.blit(self.duration_txt, duration_rect)
            self.duration_selector.draw(
                screen,
                (s_rect.midbottom[0], s_rect.midbottom[1] - 120),
                self.preferences["duration"],
                self.mouse_pos,
                self.events,
                self.theme.error_color,
            )
            self.preferences["duration"] = self.duration_selector.chosen_duration
