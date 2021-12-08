from typing import List, Tuple


color_count = 0


def return_color(color: List[int], direction: str, dt: float) -> Tuple[list, str]:
    """
    :param color: Color to be incremented.
    :param direction: Increment/decrement variable
    :param dt: Delta time. Amount of time taken last frame.

    This function returns the increment/decrement of the next RGB
    value, causing dynamic and aesthetic coloring effects.
    """

    global color_count

    r, g, b = color

    if color_count <= 100:
        color_count += dt * 100

    else:
        if direction == "up":
            if r < 255:
                r += 1
            elif g < 255:
                g += 1
            elif b < 255:
                b += 1
            else:
                direction = "down"
        else:
            if r > 0:
                r -= 1
            elif g > 0:
                g -= 1
            elif b > 0:
                b -= 1
            else:
                direction = "up"
        color_count = 0

    color = [r, g, b]

    return color, direction
