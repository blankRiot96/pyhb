import pygame
import time
from pyhb.typing_tester.display import *
from pyhb.typing_tester.settings import Settings
from pyhb.typing_tester.text_manager import TextManager
from pyhb.typing_tester.cursor import Cursor
from pyhb.typing_tester.dynamic_color import return_color
from pyhb.typing_tester.exp_circle import ExpandingCircles
from pyhb.typing_tester.settings import Settings


def main():
    # Connecting vars
    color = [0, 0, 0]
    direction = "up"
    clicks = 0

    # Event vars
    c_event = False
    exp_event = False

    # Object init
    console = TextManager(screen, punctuation=False, color=(255, 255, 255))
    cursor = Cursor(color, 2)
    expanding_circles = ExpandingCircles(
        init_radius=5, max_radius=40, increment=3, colour=(255, 255, 255), width=10
    )
    bg_color = (35, 0, 64)
    settings = Settings()


    # Time variables
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


        # Event handler
        # c_event = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1

            if event.type == pygame.MOUSEBUTTONUP:
                clicks += 1

        # print(c_event)
        if clicks == 2:
            clicks = 0
            exp_event = True
        else:
            exp_event = False

        # Draw background
        screen.fill(bg_color)

        # Dynamic color
        color, direction = return_color(color, direction, dt)

        # Text console
        console.update(events, dt)
        console.draw()

        # Settings
        settings.draw(screen)

        # Click effect
        expanding_circles.update(exp_event, mouse_pos)
        expanding_circles.draw(screen, dt)

        # Cursor
        cursor.colour = color
        cursor.update(*mouse_pos, screen, dt)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
