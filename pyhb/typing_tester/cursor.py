import pygame
from typing import Union, List, Tuple
import random


def circle_surf(radius, color) -> pygame.Surface:
    surf = pygame.Surface((int(radius * 2), int(radius * 2)))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))

    return surf


class Particle:
    def __init__(
        self,
        start_x,
        start_y,
        speed,
        mode,
        shape,
        size: List[int],
        colour: Tuple[int, int, int],
        prange: Tuple[float, float],
        acceleration=False,
        glow=True,
    ):
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.mode = mode
        self.shape = shape
        self.size = size
        self.colour = colour
        self.increase = random.uniform(*prange)
        self.acceleration = acceleration
        self.glow = glow

        self.dt = 0

    def update(self, dt):
        self.dt = dt

        # Reduce Particle Size
        self.size[0] -= 0.3 * self.dt
        self.size[1] -= 0.3 * self.dt

        if self.mode == "classic":
            self.classic()
        elif self.mode == "crazy":
            self.crazy()

    def classic(self):
        self.x += self.increase * self.dt
        self.y -= self.speed * self.dt

    def crazy(self):
        self.x += random.randrange(-3, 3) * self.speed
        self.y += random.randrange(-3, 3) * self.speed

    def draw(self, screen):
        rect = pygame.Rect((self.x, self.y), self.size)
        rect.center = (self.x, self.y)

        if self.shape == "rectangle":
            pygame.draw.rect(screen, self.colour, rect)
        elif self.shape == "circle":
            pygame.draw.circle(
                screen, self.colour, (self.x, self.y), tuple(self.size)[0]
            )

        if self.glow:
            bloom_rect = pygame.Rect(self.x, self.y, self.size[0] * 2, self.size[1] * 2)
            bloom_rect.center = (self.x, self.y)
            try:
                bloom = circle_surf(tuple(self.size)[0] * 1.2, (150, 150, 150))
            except pygame.error:
                bloom = circle_surf(1, (150, 150, 150))
            bloom.set_alpha(150)
            screen.blit(bloom, bloom_rect)


class Cursor:
    def __init__(self, colour: Union[Tuple[int, int, int], str], generation_rate: int):
        self.particles: list[Particle] = []
        self.colour = colour
        self.generation_rate = generation_rate
        self.dt = 0
        self.count = 0

    def update(self, mx, my, screen, dt):
        self.dt = dt
        self.create_new_particle(mx, my)

        for particle in self.particles:
            if particle.size[0] <= 0.4:
                self.particles.remove(particle)
            particle.update(dt)
            particle.draw(screen)

    def create_new_particle(self, mx, my):
        self.count += self.dt
        if self.count >= self.generation_rate:
            size = random.randrange(6, 11)
            self.particles.append(
                Particle(
                    mx,
                    my,
                    3,
                    "classic",
                    "circle",
                    [size, size],
                    self.colour,
                    (-0.7, 0.7),
                )
            )
            self.count = 0
