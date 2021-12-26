import pygame
from pyhb.typing_tester.themes import Theme
from typing import Tuple


class Label:
    def __init__(
        self,
        position,
        size,
        content: str,
        colour=None,
        border_colour=None,
        txt_colour=(255, 255, 255),
        shape="rectangle",
    ):
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        # self.surface.set_colorkey((0, 0, 0))
        self.content = content

        self.colour = colour or None
        self.border_colour = border_colour or None
        self.txt_colour = txt_colour
        self.shape = shape
        self.t = pygame.font.SysFont("arial", size=self.rect.size[0] // 8).render(
            content, True, self.txt_colour
        )

    def change_txt(self, txt):
        self.t = pygame.font.SysFont("arial", size=self.rect.size[0] // 8).render(
            txt, True, self.txt_colour
        )

    def draw(self, screen: pygame.Surface):
        if self.colour:
            if self.shape == "rectangle":
                pygame.draw.rect(
                    self.surface,
                    self.colour,
                    self.surface.get_rect(),
                    border_radius=1,
                    width=5,
                )
        if self.border_colour:
            pygame.draw.rect(
                self.surface,
                self.border_colour,
                self.surface.get_rect(),
                border_radius=4,
                width=1,
            )

        screen.blit(self.surface, self.rect)
        screen.blit(self.t, self.t.get_rect(center=self.rect.center))


class Toggle:
    def __init__(self, size: Tuple[int, int]):
        self.size = size

        # Make rounded Surface
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0, 0, 0))

        # Color variables
        self.grey = 100
        self.color = (self.grey, self.grey, self.grey)
        self.hover_border_color = pygame.Color("yellow")
        self.hover_border_width = 2

        # Flags

        # Rectangles
        self.rect = pygame.Rect((0, 0), self.size)
        self.pos_rect = pygame.Rect((0, 0), self.size)
        self.radius = self.size[1] // 2
        self.whole_rect = pygame.Rect(
            (0, 0), (self.rect.width + 2 * self.radius, self.rect.height)
        )
        self.hover_border_rect = pygame.Rect(
            (0, 0),
            (
                self.size[0] + self.hover_border_width * 2,
                self.size[1] + self.hover_border_width * 2,
            ),
        )

        # Toggle circle thingy
        self.toggle_circle_radius = self.radius - 5
        self.toggle_circle_rect = pygame.Rect(
            (0, 0), (self.toggle_circle_radius, self.toggle_circle_radius)
        )
        self.toggle_x = 0

        # Information
        self.label = Label(
            self.rect.center,
            (40 * 2.5, 10 * 2.5),
            "punctuation: ",
            colour="black",
            border_colour="white",
        )
        self.animation_speed = 3

        # Flags
        self.switch = False
        self.transition = False
        self.hover = False
        self.initial_pos = True

        # Count variables
        self.dt = 0

    def update(self, mouse_pos: Tuple[int, int], events, dt):
        self.dt = dt

        self.hover = self.whole_rect.collidepoint(mouse_pos)

        for event in events:
            if self.hover:
                self.label.rect.topleft = mouse_pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.switch = not self.switch

        # Animate toggle
        if self.switch:
            if self.toggle_circle_rect.x < self.pos_rect.midright[0]:
                self.toggle_x += self.animation_speed * self.dt
        else:
            if self.toggle_circle_rect.x > self.pos_rect.midleft[0]:
                self.toggle_x -= self.animation_speed * self.dt
        self.toggle_circle_rect.x = self.toggle_x

    def transition_fade(self) -> None:
        r, g, b = self.color

        # r = 100, g = 100, b = 100
        if self.switch:
            if r > 0:
                r -= 1
            if g < 255:
                g += 1
            if b > 0:
                b -= 1
        # r = 0, g = 255, b = 0
        else:
            if r < 100:
                r += 1
            if g > 100:
                g -= 1
            if b < 100:
                b += 1

        self.color = (r, g, b)

    def draw(self, screen: pygame.Surface, pos: Tuple[int, int], resize_frame: bool):
        self.surf.fill((0, 0, 0))
        self.transition_fade()
        # s_rect = screen.get_rect()

        # Positioning widgets
        self.pos_rect.topleft = pos
        self.whole_rect.center = self.pos_rect.center
        self.hover_border_rect.center = self.pos_rect.center

        if resize_frame:
            self.initial_pos = True

        if self.initial_pos:
            if self.switch:
                self.toggle_x = self.pos_rect.midright[0]
            else:
                self.toggle_x = self.pos_rect.midleft[0]
            self.toggle_circle_rect.x = self.toggle_x
            self.initial_pos = False
        self.toggle_circle_rect.y = self.pos_rect.midleft[1] - 2

        # Hover yellow borderline effect
        if self.hover:
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midleft,
                self.radius + self.hover_border_width,
            )
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midright,
                self.radius + self.hover_border_width,
            )

            pygame.draw.rect(screen, self.hover_border_color, self.hover_border_rect)

        pygame.draw.circle(
            screen,
            self.color,
            self.pos_rect.midleft,
            self.radius,
        )
        pygame.draw.circle(screen, self.color, self.pos_rect.midright, self.radius)

        pygame.draw.rect(self.surf, self.color, self.rect)
        screen.blit(self.surf, pos)

        # Draw toggle circle thingy
        pygame.draw.circle(
            screen,
            "white",
            center=self.toggle_circle_rect.center,
            radius=self.toggle_circle_radius,
        )

        # Widget information
        if self.hover:
            content = "on" if self.switch else "off"
            self.label.change_txt(f"punctuation: {content}")
            self.label.draw(screen)


class ThemeWidget:
    def __init__(self, title, size) -> None:
        self.theme = Theme(title)
        self.title = self.theme._id
        self.size = size
        self.width, self.height = self.size
        self.color = self.theme.bg_color
        self.select_color = pygame.Color("yellow")
        self.rect = pygame.Rect((0, 0), size)

        # Rects
        self.hover_pad = 3
        self.hover_rect = pygame.Rect((0, 0), (self.size[0] + self.hover_pad, self.size[1] + self.hover_pad))

        # Information widget
        self.label = Label(
            self.rect.center,
            (40 * 2.5, 10 * 2.5),
            self.title,
            colour="black",
            border_colour="white",
        )
        self.hover = False
        self.clicked = False

    def update(self, events, mouse_pos) -> None:
        # Show information on hover
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.hover:
            self.label.rect.topleft = mouse_pos

        for event in events:
            if self.hover:
                self.clicked = event.type == pygame.MOUSEBUTTONDOWN

    def draw_label(self, screen):
        if self.hover:
            self.label.draw(screen)

    def draw(self, screen, pos) -> None:
        self.rect.topleft = pos
        self.hover_rect.topleft = (pos[0] - self.hover_pad, pos[1] - self.hover_pad)
        pygame.draw.rect(screen, self.color, self.rect)
        if self.hover:
            pygame.draw.rect(screen, self.select_color, self.hover_rect, width=self.hover_pad)


class ThemeSelection:
    def __init__(self, theme):
        self.theme = theme
        self.theme_widget_size = (25, 25)
        self.theme_widget_padding = 20
        self.theme_widgets = [
            ThemeWidget(title, self.theme_widget_size) for title in self.theme.themes
        ]

        total_width = 4 * (self.theme_widget_size[0] + self.theme_widget_padding)
        total_height = 2 * (self.theme_widget_padding + self.theme_widget_size[1])
        self.surf = pygame.Surface((total_width, total_height))
        self.surf_rect = self.surf.get_rect()

    def draw(self, screen: pygame.Surface, mouse_pos, pos, events):
        self.surf_rect.center = pos
        start_pos = self.surf_rect.topleft

        for index, theme_widget in enumerate(self.theme_widgets):
            y_increment = 0 if index < 4 else 1

            index = index - 4 if y_increment else index
            theme_widget.update(events, mouse_pos)
            theme_widget.draw(
                screen,
                (
                    index * (theme_widget.width + self.theme_widget_padding)
                    + start_pos[0],
                    (y_increment * (theme_widget.height + self.theme_widget_padding)) + start_pos[1],
                ),
            )

            if theme_widget.title == self.theme._id:
                pygame.draw.rect(screen, "green", theme_widget.hover_rect, width=theme_widget.hover_pad)

            if theme_widget.clicked:
                self.theme = theme_widget.theme

        for theme_widget in self.theme_widgets:
            theme_widget.draw_label(screen)

        # screen.blit(self.surf, self.surf_rect)


class DurationSelection:
    def __init__(self, theme, duration):
        self.theme = theme
        self.font = pygame.font.SysFont("arialrounded", 25)
        self.durations = (15, 30, 45, 60)
        self.duration_txts = tuple(
            (self.font.render(str(duration), True, theme.error_color) for duration in self.durations)
        )
        self.duration_txts_rects = tuple((duration_txt.get_rect() for duration_txt in self.duration_txts))
        self.padding = 15

        self.chosen_duration = duration
        self.clicked = False

    def draw(self, screen, start_pos, console_duration, mouse_pos, events, error_color):
        self.duration_txts = tuple(
            (self.font.render(str(duration), True, error_color) for duration in self.durations)
        )

        for event in events:
            self.clicked = event.type == pygame.MOUSEBUTTONDOWN

        for index, duration_rect in enumerate(self.duration_txts_rects):
            centering = 2 * (duration_rect.width + self.padding)
            duration_rect.topleft = (start_pos[0] + (index * (duration_rect.width + self.padding)) - centering,
                                     start_pos[1])

        for duration, duration_rect in zip(self.duration_txts, self.duration_txts_rects):
            if duration_rect.collidepoint(mouse_pos):
                duration.set_alpha(100)
                if self.clicked:
                    self.chosen_duration = self.durations[self.duration_txts.index(duration)]
            else:
                duration.set_alpha(255)

            screen.blit(duration, duration_rect)

            if console_duration == self.durations[self.duration_txts.index(duration)]:
                rect = pygame.Rect((0, 0),
                                   (duration_rect.width + 10,
                                    duration_rect.height + 10))
                rect.center = duration_rect.center
                pygame.draw.rect(screen, self.theme.font_color, rect, width=2)

