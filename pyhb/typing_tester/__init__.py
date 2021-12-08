import pygame
import time
from pyhb.typing_tester.display import *
from pyhb.typing_tester.passage_generator import get_sentences
from pyhb.typing_tester.words import words


def main():
    # Fonts
    font = pygame.font.SysFont("leelawadee", 25)

    # Text variables
    correct_lines = [
        "something very very very cool thirty not is a",
        "thats not very cool because i say so, idk if ",
        "you dont think so, because what i say is what"
    ]
    lines = [""]
    correct_text = " ".join(correct_lines)
    user_text = ""
    cursor = "|"

    # Count variables
    index = 0
    count_vars = {
        "cursor": 0,
        "delete": 0,
    }

    # Cooldown variables
    cooldowns = {
        "cursor": 33,
        "delete": 4
    }

    # Booleans/Flags
    delete = False
    show_shadow = True

    # Time variables
    start = time.time()

    run = True
    while run:
        clock.tick()

        # Calculating Delta Time
        end = time.perf_counter()

        dt = end - start
        dt *= FPS

        start = time.perf_counter()

        # Handling count variables
        if count_vars['delete'] <= cooldowns['delete']:
            delete = False

        for count in count_vars:
            count_vars[count] += dt

            if count_vars[count] >= cooldowns[count]:
                count_vars[count] = 0

                if count == "cursor":
                    cursor = "|" if cursor == "" else ""
                if count == "delete":
                    delete = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and delete:
            cursor = "|"
            try:
                user_text = user_text[:-1]
                lines[index] = lines[index][:-1]
                if index != 0:
                    if lines[index] == "":
                        del lines[index]
                        index -= 1
            except IndexError:
                pass

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                cursor = "|"
                if not event.key == pygame.K_BACKSPACE:
                    try:
                        user_text += chr(event.key)
                        lines[index] += chr(event.key)
                    except ValueError:
                        pass
                if user_text == correct_text[:len(user_text)]:
                    show_shadow = True
                else:
                    show_shadow = False

                if len(user_text) % 45 == 0:
                    lines.append("")
                    index += 1

        # Draw background
        screen.fill((35, 0, 64))
        # win.fill((34, 0, 64))

        # todo
        # If len(user_text) == 45
        # Make a new line
        if show_shadow:
            for _index, line in enumerate(correct_lines):
                shadow_text = font.render(line, True, "white")
                shadow_rect = shadow_text.get_rect(center=screen.get_rect().center)
                shadow_text.set_alpha(150)

                
                screen.blit(shadow_text, (shadow_rect.topleft[0], shadow_rect.topleft[1] + _index*shadow_text.get_height()))

        for _index, line in enumerate(lines):
            if line == lines[-1]:
                eptic = line + cursor
            else:
                eptic = line

            # Create text surfaces
            text = font.render(eptic, True, "white")

            # Draw text
            screen.blit(text, (shadow_rect.topleft[0], shadow_rect.topleft[1] + _index*shadow_text.get_height()))

        # win.blit(screen, (50, 50))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
