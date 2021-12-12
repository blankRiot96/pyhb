import pygame
from typing import List, Tuple


class ExpandingCircle:
    def __init__(
        self,
        pos: Tuple[int, int],
        init_radius,
        max_radius,
        increment: float,
        colour: Tuple[int, int, int],
        width: int = 10,
    ):
        self.pos = pos
        self.radius = init_radius
        self.max_radius = max_radius
        self.increment = increment
        self.colour = colour
        self.width = width

        self.cool_down = 7
        self.count = 0

    def draw(self, screen, dt):
        self.count += dt
        if self.radius <= self.max_radius:
            self.radius += self.increment * dt

            if self.count >= self.cool_down:
                self.width -= 1

            # Make sure that width is valid value for circle
            if self.width <= 0:
                self.width = 1

            pygame.draw.circle(
                screen, self.colour, self.pos, self.radius, width=self.width
            )


class ExpandingCircles:
    def __init__(
        self,
        init_radius,
        max_radius,
        increment: float,
        colour: Tuple[int, int, int],
        width: int = 10,
    ) -> None:
        self.circles: List[ExpandingCircle] = []
        self.init_radius = init_radius
        self.max_radius = max_radius
        self.increment = increment
        self.color = colour
        self.width = width

    def update(self, events, pos: Tuple[int, int]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                    self.circles.append(
                        ExpandingCircle(
                            pos,
                            self.init_radius,
                            self.max_radius,
                            self.increment,
                            self.color,
                            width=self.width,
                        )
                    )

    def draw(self, screen, dt) -> None:
        for circle in self.circles:
            circle.draw(screen, dt)
            if circle.width <= 0:
                self.circles.remove(circle)
