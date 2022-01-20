"""
Main file for the HeartBeat typing test
Coordinates all related objects within its main loop.
"""

import time
import pygame
from pyhb.typing_tester.settings import Settings
from pyhb.typing_tester.text_manager import TextManager
from pyhb.typing_tester.cursor import Cursor
from pyhb.typing_tester.dynamic_color import return_color
from pyhb.typing_tester.exp_circle import ExpandingCircles
from pyhb.typing_tester.settings import Settings


def main(screen, clock, FPS):
    settings = Settings(screen)

    # Connecting vars
    color = [0, 0, 0]
    bg_color = settings.theme.bg_color
    direction = "up"
    state = "typing_test"

    # Object init
    console = TextManager(
        screen,
        punctuation=settings.preferences["punctuation"],
        color=(255, 255, 255),
        duration=settings.preferences["duration"],
    )
    cursor = Cursor(color, 2)
    expanding_circles = ExpandingCircles(
        init_radius=5, max_radius=40, increment=3, colour=(255, 255, 255), width=10
    )

    # Set theme
    settings.theme.set_theme(settings, console, (0, 0, 0))

    # Comparison frame values
    last_screen_center = screen.get_rect().center
    last_theme = settings.theme._id
    current_s_icon_color = (0, 0, 0)
    start = time.perf_counter()

    run = True
    while run:
        clock.tick()

        # Calculating Delta Time
        end = time.perf_counter()

        dt = end - start
        dt *= FPS
        start = time.perf_counter()

        # Mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check if screen has been resized
        current_screen_center = screen.get_rect().center
        resize_frame = current_screen_center != last_screen_center
        last_screen_center = screen.get_rect().center

        # Check if theme has been changed
        current_theme = settings.theme._id
        if current_theme != last_theme:
            settings.theme.set_theme(settings, console, current_s_icon_color)
            bg_color = settings.theme.bg_color
            settings.punctuation_txt = settings.font.render("Punctuation", True, settings.theme.font_color)
            settings.theme_txt = settings.font.render("Themes", True, settings.theme.font_color)
            current_s_icon_color = settings.theme.settings_icon_color

        last_theme = settings.theme._id

        # Event handler
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                settings.save_preferences(list(screen.get_rect().size))
                run = False

        # Draw background
        screen.fill(bg_color)

        # Dynamic color
        color, direction = return_color(color, direction, dt)

        if state == "typing_test":
            settings.img = settings.settings_icon
            settings.label.change_txt("settings")
            # Text console
            console.update(events, dt, resize_frame)
            console.draw()

            if console.show_results:
                settings.state = "settings"
        elif state == "settings":
            settings.img = settings.retry_icon
            settings.label.change_txt("retry")
            if console.show_results:
                console.get_results(resize_frame, color)
            if settings.start_animation and not settings.expanding:
                console.show_results = False
                console = TextManager(
                    screen,
                    punctuation=settings.preferences["punctuation"],
                    color=settings.theme.font_color,
                    duration=settings.preferences["duration"],
                )

        # Settings
        settings.update(mouse_pos, events, dt)
        settings.draw(screen, resize_frame)

        state = settings.state

        # Click effect
        expanding_circles.update(events, mouse_pos)
        expanding_circles.draw(screen, dt)

        # Cursor
        cursor.colour = color
        cursor.update(*mouse_pos, screen, dt)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    from pyhb.typing_tester.display import *
    main(screen, clock, FPS)
