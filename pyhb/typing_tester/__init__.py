import time

import pygame

from pyhb.typing_tester.display import *


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
    print(correct_text)
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
        end = time.time()

        dt = end - start
        dt *= 60

        start = time.time()

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

        # todo
        # If len(user_text) == 45
        # Make a new line
        if show_shadow:
            for line in correct_lines:
                shadow_text = font.render(line, True, "white")
                shadow_text.set_alpha(150)
                screen.blit(shadow_text, (screen_width // 4, (screen_height // 4) + correct_lines.index(line) * 30))

        for line in lines:
            if line == lines[-1]:
                eptic = line + cursor
            else:
                eptic = line

            # Create text surfaces
            text = font.render(eptic, True, "white")

            # Draw text
            screen.blit(text, (screen_width // 4, (screen_height // 4) + lines.index(line) * 30))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
