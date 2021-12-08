import pygame
import time
from pyhb.typing_tester.display import *
from pyhb.typing_tester.text_manager import TextManager


def main():
    # Text Manager class
    console = TextManager(screen, punctuation=False, color=(255, 255, 255))

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

        # Draw background
        screen.fill((35, 0, 64))

        # Text console
        console.update(dt)
        console.draw()


        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
