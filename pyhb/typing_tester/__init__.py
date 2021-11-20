import time
from pyhb.typing_tester.display import *


def main():
    # Fonts
    font = pygame.font.SysFont("leelawadee", 25)

    # Text variables
    correct_text = "something very cool"
    user_text = ""
    cursor = "|"

    # Count variables
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
                    except ValueError:
                        pass
                if user_text == correct_text[:len(user_text)]:
                    show_shadow = True
                else:
                    show_shadow = False

        # Draw background
        screen.fill((35, 0, 64))

        # todo
        # If len(user_text) == 45
        # Make a new line

        # Draw text
        shadow_text = font.render(correct_text, True, "white")
        text = font.render(user_text + cursor, True, "white")

        shadow_text.set_alpha(150)
        if show_shadow:
            screen.blit(shadow_text, (screen_width//4, screen_height//4))
        screen.blit(text, (screen_width//4, screen_height//4))

        pygame.display.update()

    pygame.quit()


